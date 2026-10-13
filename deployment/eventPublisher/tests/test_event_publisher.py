import copy
import logging
import sys
from unittest.mock import MagicMock

import asn1tools
import EventPublisher
import pytest


@pytest.fixture
def client_and_mocks():
    encoder = MagicMock()
    encoder.encode.return_value = b"\x01\x02\x03"
    producer = MagicMock()
    app = EventPublisher.create_app(producer=producer, encoder=encoder)
    app.config.update(TESTING=True)
    return app.test_client(), encoder, producer


def test_publish_valid_message(client_and_mocks):
    client, encoder, producer = client_and_mocks
    resp = client.post("/api/publish/denm/public/7y0191k4", json={"a": 1})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["sub_service"] == "DENM"
    assert body["key"] == "v2x/denm/public/g8/7/y/0/1/9/1/k/4"
    encoder.encode.assert_called_once()
    producer.produce.assert_called_once()
    producer.flush.assert_called_once()


def test_delivery_report_callback_branches(client_and_mocks):
    client, _encoder, producer = client_and_mocks
    client.post("/api/publish/denm/public/7y0191k4", json={"a": 1})
    callback = producer.produce.call_args.kwargs["callback"]
    # success branch (err is None) and failure branch
    callback(None, MagicMock())
    callback(Exception("boom"), MagicMock())


def test_invalid_sub_service(client_and_mocks):
    client, _, _ = client_and_mocks
    resp = client.post("/api/publish/unknown/public/7y0191k4", json={"a": 1})
    assert resp.status_code == 400


def test_invalid_sub_service_group(client_and_mocks):
    client, _, _ = client_and_mocks
    resp = client.post("/api/publish/denm/bad.group/7y0191k4", json={"a": 1})
    assert resp.status_code == 400


def test_invalid_geohash(client_and_mocks):
    client, _, _ = client_and_mocks
    # a, i, l, o are not part of the geohash base32 alphabet
    resp = client.post("/api/publish/denm/public/ailo", json={"a": 1})
    assert resp.status_code == 400


def test_body_must_be_json_object(client_and_mocks):
    client, _, _ = client_and_mocks
    resp = client.post("/api/publish/denm/public/7y0191k4", json=[1, 2, 3])
    assert resp.status_code == 400


def test_encode_error_returns_400(client_and_mocks):
    client, encoder, _ = client_and_mocks
    encoder.encode.side_effect = asn1tools.codecs.EncodeError("bad payload")
    resp = client.post("/api/publish/denm/public/7y0191k4", json={"a": 1})
    assert resp.status_code == 400


def test_payload_too_large():
    app = EventPublisher.create_app(producer=MagicMock(), encoder=MagicMock())
    app.config["MAX_CONTENT_LENGTH"] = 10
    client = app.test_client()
    resp = client.post(
        "/api/publish/denm/public/7y0191k4",
        data=b"x" * 50,
        content_type="application/json",
    )
    assert resp.status_code == 413


def test_build_encoder_reads_asn_folder():
    encoder = EventPublisher.build_encoder()
    assert encoder is not None


def test_build_producer_lazy_import(monkeypatch):
    fake_module = MagicMock()
    monkeypatch.setitem(sys.modules, "confluent_kafka", fake_module)
    producer = EventPublisher.build_producer()
    assert producer is fake_module.Producer.return_value


def test_configure_logging_writes_logfile(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    EventPublisher.configure_logging()
    assert (tmp_path / "app.log").exists()


# --- Log sanitisation (CWE-117) ---


class _RecordCollector(logging.Handler):
    """Capture records emitted by a specific logger, independent of caplog propagation."""

    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


def test_sanitize_for_log_strips_newlines():
    result = EventPublisher.sanitize_for_log("first\r\n2026-01-01 INFO forged entry")
    assert "\r" not in result
    assert "\n" not in result
    # Only the line breaks go; the surrounding text is preserved for debuggability.
    assert result == "first2026-01-01 INFO forged entry"


def test_sanitize_for_log_strips_control_chars():
    # NUL, ESC (ANSI escape sequences) and a C1 control.
    result = EventPublisher.sanitize_for_log("a\x00b\x1b[31mc\x85d")
    assert result == "ab[31mcd"


def test_sanitize_for_log_truncates():
    result = EventPublisher.sanitize_for_log("x" * 1000)
    assert result == "x" * EventPublisher.LOG_VALUE_MAX_LENGTH + "...[truncated]"


def test_sanitize_for_log_accepts_non_str():
    assert EventPublisher.sanitize_for_log(ValueError("boom\nsecond")) == "boomsecond"


def test_encode_error_message_is_sanitized():
    """The ASN.1 error message embeds values from the unvalidated request body."""
    encoder = MagicMock()
    encoder.encode.side_effect = asn1tools.codecs.EncodeError("bad\r\n2026-01-01 INFO forged entry")
    app = EventPublisher.create_app(producer=MagicMock(), encoder=encoder)

    collector = _RecordCollector()
    previous_level = app.logger.level
    app.logger.addHandler(collector)
    app.logger.setLevel(logging.WARNING)
    try:
        resp = app.test_client().post("/api/publish/denm/public/7y0191k4", json={"a": 1})
    finally:
        app.logger.removeHandler(collector)
        app.logger.setLevel(previous_level)

    assert resp.status_code == 400
    warnings = [r for r in collector.records if r.levelno == logging.WARNING]
    assert len(warnings) == 1
    message = warnings[0].getMessage()
    assert "\r" not in message
    assert "\n" not in message
    assert "forged entry" in message


def test_publish_logs_sanitized_key():
    encoder = MagicMock()
    encoder.encode.return_value = b"\x01\x02\x03"
    app = EventPublisher.create_app(producer=MagicMock(), encoder=encoder)

    collector = _RecordCollector()
    previous_level = app.logger.level
    app.logger.addHandler(collector)
    app.logger.setLevel(logging.INFO)
    try:
        resp = app.test_client().post("/api/publish/denm/public/7y0191k4", json={"a": 1})
    finally:
        app.logger.removeHandler(collector)
        app.logger.setLevel(previous_level)

    assert resp.status_code == 200
    key_lines = [r.getMessage() for r in collector.records if r.getMessage().startswith("key: ")]
    assert key_lines == ["key: v2x/denm/public/g8/7/y/0/1/9/1/k/4"]


# --- Real ASN.1 encoder (exercises the asn1tools version pinned in requirements.txt) ---

# The reference DENM from docs/HTTP-Integration-Testing.md and its UPER encoding. If an
# asn1tools upgrade changes these bytes, subscribers would receive a different payload.
REFERENCE_DENM = {
    "header": {"protocolVersion": 2, "messageID": 1, "stationID": 123456},
    "denm": {
        "management": {
            "actionID": {"originatingStationID": 123456, "sequenceNumber": 1},
            "detectionTime": 649940045094,
            "referenceTime": 649940045094,
            "eventPosition": {
                "latitude": 367225309,
                "longitude": -43965883,
                "positionConfidenceEllipse": {
                    "semiMajorConfidence": 4095,
                    "semiMinorConfidence": 4095,
                    "semiMajorOrientation": 3601,
                },
                "altitude": {"altitudeValue": 0, "altitudeConfidence": "unavailable"},
            },
            "relevanceDistance": "lessThan500m",
            "validityDuration": 60,
            "stationType": 10,
        },
        "situation": {"informationQuality": 0, "eventType": {"causeCode": 95, "subCauseCode": 0}},
        "location": {
            "eventPositionHeading": {"headingValue": 0, "headingConfidence": 127},
            "traces": [[{"pathPosition": {"deltaLatitude": 2117, "deltaLongitude": 5821, "deltaAltitude": 0}}]],
        },
    },
}
REFERENCE_DENM_UPER_HEX = (
    "02010001e240c50000f120000092ea6e41a4c4ba9b906934b8852dd68aaf445ffffffe11186a0f6003c0a00be004001f8028211216bc6338"
)


@pytest.fixture(scope="module")
def real_encoder():
    return EventPublisher.build_encoder()


@pytest.fixture
def real_client(real_encoder):
    producer = MagicMock()
    app = EventPublisher.create_app(producer=producer, encoder=real_encoder)
    app.config.update(TESTING=True)
    return app.test_client(), producer


def _reference_denm_with(path, value):
    body = copy.deepcopy(REFERENCE_DENM)
    target = body
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return body


def test_reference_denm_encodes_to_known_bytes(real_client):
    client, producer = real_client
    resp = client.post("/api/publish/denm/public/7y0191k4", json=REFERENCE_DENM)
    assert resp.status_code == 200
    assert producer.produce.call_args.kwargs["key"] == "v2x/denm/public/g8/7/y/0/1/9/1/k/4"
    assert producer.produce.call_args.kwargs["value"] == REFERENCE_DENM_UPER_HEX


@pytest.mark.parametrize(
    "path, value",
    [
        # asn1tools raises a different exception for each; all are client errors (400), not 500.
        (("denm",), None),  # EncodeError: wrong type for a SEQUENCE
        (("denm", "management", "relevanceDistance"), "nope"),  # KeyError: unknown ENUMERATED value
        (("denm", "management", "validityDuration"), "sixty"),  # TypeError: string in an INTEGER field
    ],
    ids=["encode-error", "unknown-enum", "string-for-integer"],
)
def test_schema_mismatch_returns_400(real_client, path, value):
    client, producer = real_client
    resp = client.post("/api/publish/denm/public/7y0191k4", json=_reference_denm_with(path, value))
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "payload does not conform to the message schema"}
    producer.produce.assert_not_called()
