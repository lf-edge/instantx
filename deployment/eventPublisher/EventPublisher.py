# ========================LICENSE_START=================================
# Event Publisher
# %%
# Copyright (C) 2024 - 2025 Vodafone
# %%
# Licensed under the MIT License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://opensource.org/license/mit
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================LICENSE_END==================================

import logging
import os
import random
import re
import time
from binascii import hexlify

import asn1tools
import config as config
from flask import Flask, jsonify, request
from prometheus_client import Counter, start_http_server

# Prometheus metric (registered once at import time).
REQUEST_COUNT = Counter(config.MESSAGES_COUNT_METRICS, "Number of messages processed", ["sub_service"])

# --- Input-validation allowlists ---
# Geohash base32 alphabet (excludes a, i, l, o); 1-12 characters.
GEOHASH_RE = re.compile(r"^[0-9bcdefghjkmnpqrstuvwxyz]{1,12}$")
# Service group: lowercase alphanumerics, dash/underscore, up to 32 chars.
SUB_SERVICE_GROUP_RE = re.compile(r"^[a-z0-9_-]{1,32}$")
# Supported sub-services (message types). Configurable; defaults to DENM.
ALLOWED_SUB_SERVICES = {s.lower() for s in getattr(config, "ALLOWED_SUB_SERVICES", {"denm"})}
# Reject oversized request bodies (default 1 MiB).
MAX_CONTENT_LENGTH = getattr(config, "MAX_CONTENT_LENGTH", 1 * 1024 * 1024)


def build_encoder(data_folder=None):
    """Compile the ASN.1 schemas used to UPER-encode messages."""
    data_folder = data_folder or os.path.join(os.path.dirname(__file__), "asn")
    asn1_files = [
        os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".asn")
    ]
    return asn1tools.compile_files(
        asn1_files,
        codec="uper",
        any_defined_by_choices=None,
        encoding="utf-8",
        numeric_enums=False,
    )


def build_producer():
    """Create the Kafka producer. Imported lazily so the module is importable without librdkafka."""
    from confluent_kafka import Producer

    return Producer({"bootstrap.servers": config.KAFKA_BROKER})


def configure_logging():
    """Configure application logging. Called from the entrypoint, not on import."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
        handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
        force=True,
    )


def create_app(producer=None, encoder=None):
    """Application factory. Dependencies are injectable so the app is unit-testable."""
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    if encoder is None:
        encoder = build_encoder()
    if producer is None:
        producer = build_producer()

    def delivery_report(err, msg):
        if err is not None:
            app.logger.error("Message delivery failed: %s", err)
        else:
            app.logger.info("Message delivered to %s %s", msg.topic(), msg.partition())

    def send_message(data, key):
        producer.produce(config.KAFKA_TOPIC, key=key, value=data, callback=delivery_report)
        producer.flush()  # Ensure the message is sent before returning

    @app.route(
        "/api/publish/<string:sub_service>/<string:sub_service_group>/<string:geohash>",
        methods=["POST"],
    )
    def publish_message(sub_service, sub_service_group, geohash):
        app.logger.info("Publishing endpoint reached")

        # --- Validate all untrusted inputs against allowlists before use ---
        if sub_service.lower() not in ALLOWED_SUB_SERVICES:
            return jsonify({"error": "unsupported sub_service"}), 400
        if not SUB_SERVICE_GROUP_RE.match(sub_service_group):
            return jsonify({"error": "invalid sub_service_group"}), 400
        if not GEOHASH_RE.match(geohash):
            return jsonify({"error": "invalid geohash"}), 400

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "request body must be a JSON object"}), 400

        geo_level = str(len(geohash))
        geohash_path = "/".join(list(geohash))
        key = f"v2x/{sub_service}/{sub_service_group}/g{geo_level}/{geohash_path}"
        app.logger.info("key: %s", key)

        message_type = sub_service.upper()
        try:
            encoded = encoder.encode(message_type, data)
        except asn1tools.codecs.EncodeError as exc:
            app.logger.warning("Encoding failed: %s", exc)
            return jsonify({"error": "payload does not conform to the message schema"}), 400

        message = hexlify(encoded).decode("ascii")
        app.logger.debug("Encoded: %s", message)

        time.sleep(random.uniform(0.5, 1.5))  # nosec B311 - non-crypto timing jitter
        REQUEST_COUNT.labels(sub_service=message_type).inc()

        send_message(message, key)

        return jsonify(
            {
                "sub_service": message_type,
                "key": key,
                "topic": f"{config.KAFKA_TOPIC}",
                "message": "Message processed successfully",
            }
        )

    return app


if __name__ == "__main__":
    from waitress import serve

    configure_logging()
    application = create_app()
    # Start the Prometheus metrics server
    start_http_server(config.PROMETHEUS_SERVER)
    # Start the Waitress server (production)
    serve(application, host="0.0.0.0", port=config.port)  # nosec B104 - containerized service, published port
