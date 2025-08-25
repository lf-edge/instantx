FROM python:3.9-slim

WORKDIR /app

COPY kafka_speed_exporter.py /app/

RUN pip install kafka-python prometheus_client

EXPOSE 8010

CMD ["python", "kafka_speed_exporter.py"]
