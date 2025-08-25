from kafka import KafkaConsumer
from prometheus_client import Gauge, start_http_server
import json

# Metric with stationID
speed_metric = Gauge('station_speed_kph', 'Velocidad reportada por estación', ['stationID'])

# Prometheus Server
start_http_server(8010)

# Kafka Consumer
consumer = KafkaConsumer(
    'agl-grafana-metrics',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='prometheus-speed-exporter'
)
print("consumer")

# Principal loop to consume messages
for message in consumer:
    try:
        data = message.value
        station_id = data['labels']['stationID']
        speed = data['speedValue']['value']
        speed_metric.labels(stationID=station_id).set(speed)
        print("success")
    except Exception as e:
        print(f"Error procesando mensaje: {e}")
