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

from flask import Flask, jsonify, request
from binascii import hexlify
from prometheus_client import start_http_server, Summary, Counter
from confluent_kafka import Producer
from waitress import serve
import asn1tools
import os
import config as config
import time
import random
import logging

app = Flask(__name__)

# Set up logging
#logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),
                        logging.StreamHandler()
                    ])

# Kafka producer configuration
producer = Producer({
    'bootstrap.servers': config.KAFKA_BROKER
})

DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'asn')
asn1_files = [os.path.join(DATA_FOLDER, f) for f in os.listdir(DATA_FOLDER) if f.endswith('.asn')]
encoder = asn1tools.compile_files(asn1_files, codec='uper', any_defined_by_choices=None, encoding='utf-8', numeric_enums=False)

REQUEST_COUNT = Counter(config.MESSAGES_COUNT_METRICS, 'Number of messages processed', ['sub_service'])

# Define a callback function to handle delivery reports
def delivery_report(err, msg):
    if err is not None:
        #print(f"Message delivery failed: {err}")
        app.logger.error("Message delivery failed: %s", err)
    else:
        #print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
        app.logger.info("Message delivered to %s %s", msg.topic(), msg.partition())

# Define a POST route with path variable
@app.route('/api/publish/<string:sub_service>/<string:sub_service_group>/<string:geohash>', methods=['POST'])
def publish_message(sub_service, sub_service_group, geohash):

    app.logger.info('Publishing endpoint reached')
    app.logger.info(' - Inputs: %s, %s, %s', sub_service, sub_service_group, geohash)

    geo_level = str(len(geohash))
    geohash = '/'.join(list(geohash))

    key = 'v2x/' + sub_service + '/' + sub_service_group + '/g' + geo_level + '/' + geohash

    app.logger.info("key: %s", key)
    # Get JSON data from the request body
    data = request.get_json()
    sub_service = sub_service.upper()
    encoded = encoder.encode(sub_service, data)
    message = hexlify(encoded).decode('ascii')
    app.logger.debug('Encoded: %s', message)
    app.logger.debug('Decoded: %s', encoder.decode(sub_service, encoded, check_constraints=False))

    time.sleep(random.uniform(0.5, 1.5))
    REQUEST_COUNT.labels(sub_service=sub_service).inc()
    # Create a response
    response = {
        'sub_service': sub_service,
        'key': key,
        'topic': f'{config.KAFKA_TOPIC}',
        'message': 'Message processed successfully'
    }

    send_message(message, key)

    return jsonify(response)

def send_message(data, key):
    # Produce the message to Kafka
    producer.produce(config.KAFKA_TOPIC, key=key, value=data, callback=delivery_report)
    producer.flush()  # Ensure the message is sent before returning

    return jsonify({'status': 'Message sent successfully'})

if __name__ == '__main__':

    # Start the Prometheus metrics server
    start_http_server(config.PROMETHEUS_SERVER)
    
    # -----------------------------------
    # Start the Flask server (development)
    #app.run(host='0.0.0.0', port=config.port)
    # Start the Waitress server (production)
    serve(app, host="0.0.0.0", port=config.port)