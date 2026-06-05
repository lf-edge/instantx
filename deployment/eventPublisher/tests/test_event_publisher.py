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
