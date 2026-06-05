import json

from prometheus_client import Gauge, start_http_server

# Metric with stationID (registered once at import time).
speed_metric = Gauge("station_speed_kph", "Speed reported by station", ["stationID"])


def process_message(value, metric=speed_metric):
    """Extract stationID + speed from a decoded message and update the gauge.

    Raises KeyError/TypeError on malformed input; callers decide how to handle it.
    """
    station_id = value["labels"]["stationID"]
    speed = value["speedValue"]["value"]
    metric.labels(stationID=station_id).set(speed)
    return station_id, speed


def consume(consumer, metric=speed_metric, logger=print):
    """Consume messages and update metrics, isolating per-message failures."""
    for message in consumer:
        try:
            process_message(message.value, metric)
        except Exception as exc:  # one bad message must not stop the exporter
            logger(f"Error processing message: {exc}")


def main():  # pragma: no cover - thin wiring around external Kafka + HTTP server
    from kafka import KafkaConsumer

    start_http_server(8010)
    consumer = KafkaConsumer(
        "agl-grafana-metrics",
        bootstrap_servers="kafka:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="latest",
        group_id="prometheus-speed-exporter",
    )
    consume(consumer)


if __name__ == "__main__":
    main()
