FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY kafka_speed_exporter.py /app/

EXPOSE 8010

CMD ["python", "kafka_speed_exporter.py"]
