import types
from unittest.mock import MagicMock

import kafka_speed_exporter as exporter
import pytest


def test_process_message_sets_metric():
    metric = MagicMock()
    value = {"labels": {"stationID": "S1"}, "speedValue": {"value": 42}}
    station_id, speed = exporter.process_message(value, metric)
    assert station_id == "S1"
    assert speed == 42
    metric.labels.assert_called_once_with(stationID="S1")
    metric.labels.return_value.set.assert_called_once_with(42)


def test_process_message_raises_on_malformed():
    with pytest.raises(KeyError):
        exporter.process_message({"labels": {}}, MagicMock())


def test_consume_handles_good_and_bad_messages():
    good = types.SimpleNamespace(value={"labels": {"stationID": "S1"}, "speedValue": {"value": 10}})
    bad = types.SimpleNamespace(value={"nope": True})
    metric = MagicMock()
    logged = []
    exporter.consume([good, bad], metric=metric, logger=logged.append)
    metric.labels.assert_called_once_with(stationID="S1")
    assert len(logged) == 1  # only the malformed message is logged
    assert "Error processing message" in logged[0]
