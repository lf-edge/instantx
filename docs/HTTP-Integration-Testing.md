[Home](../README.md) > HTTP Integration Testing

# HTTP Integration Testing (Event Publisher → MQTT)

This guide walks through the real ingress path of InstantX: you POST a V2X (DENM) message to the **Event Publisher** HTTP API (`api-service`), and read the same message back from the **MQTT** broker. Following it end-to-end proves that HTTP ingress, Kafka, the MQTT Sink connector, and the broker are all wired correctly.

For raw MQTT publish/subscribe (installing the clients, broker connection details), see [Manual MQTT Testing](./MQTT-Manual-Testing.md); this guide reuses its subscriber setup.

## 1. How a message flows

```
curl  ──HTTP POST──▶  Event Publisher (api-service:5000)
                          │  validates input, UPER-encodes the DENM,
                          │  hexlifies it to an ASCII string
                          ▼
                      Kafka topic  v2x.denm.public
                          key = v2x/denm/public/g8/7/y/0/1/9/1/k/4   (the geohash path)
                          │
                          ▼  MQTTSinkConnector  (topics.regex: v2x.(cam|denm).*)
                      MQTT broker (HiveMQ)
                          topic = the Kafka key, verbatim
                          payload = the UPER hex string
                          ▼
                      mosquitto_sub -t "v2x/denm/public/g8/#"
```

Two facts that drive the rest of this guide:

- The Kafka message **key** (the geohash path) becomes the **MQTT topic**, unchanged. The Kafka topic itself is always `v2x.denm.public`.
- The MQTT **payload** is the UPER-encoded DENM rendered as a **hexadecimal string** (e.g. `02010001e240c5...`), not JSON. Decoding it back is out of scope — see [UPER Encoding](./Encoding.md).

## 2. Prerequisites

- `curl` (preinstalled on macOS / most Linux; on Windows use Git Bash, WSL, or `curl.exe`).
- The `mosquitto` clients — install per [Manual MQTT Testing § 1](./MQTT-Manual-Testing.md#1-prerequisites).
- The Docker stack running (see [section 4](#4-start--verify-the-stack)).

## 3. Connection variables

| Variable | Value | Notes |
|---|---|---|
| API base URL | `http://localhost:5000` | The `api-service` container, published as `5000:5000`. |
| Endpoint | `POST /api/publish/<sub_service>/<sub_service_group>/<geohash>` | `sub_service` must be `denm`; group matches `^[a-z0-9_-]{1,32}$`; geohash matches `^[0-9bcdefghjkmnpqrstuvwxyz]{1,12}$`. |
| Kafka topic | `v2x.denm.public` | Fixed; the geohash travels as the Kafka **key**, not in the topic name. |
| MQTT topic (result) | `v2x/denm/public/g8/7/y/0/1/9/1/k/4` | Equals the Kafka key. Subscribe with the wildcard `v2x/denm/public/g8/#`. |
| Kafka Connect REST | `http://localhost:8083` | Used to check the MQTT Sink connector status. |
| Connector name | `MQTTSinkConnector` | The Kafka → MQTT bridge; must be `RUNNING`. |

No authentication is configured on the API or the broker in the default stack (see [Manual MQTT Testing § 2](./MQTT-Manual-Testing.md#2-connection-variables)).

## 4. Start / verify the stack

From `deployment/`, bring up the full stack (the bridge needs Kafka **and** Kafka Connect, not just the broker):

```bash
cd deployment
docker-compose up -d
```

Verify the Event Publisher is reachable:

```bash
docker ps --filter "name=instantx_api-service" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Expected (truncated): `instantx_api-service   Up ...   0.0.0.0:5000->5000/tcp`.

Verify the MQTT Sink connector is `RUNNING` (it is auto-registered ~100 s after Kafka Connect starts — wait if you just launched the stack):

```bash
curl -s http://localhost:8083/connectors/MQTTSinkConnector/status
```

Expected: a JSON document whose top-level `connector.state` and each `tasks[].state` are `"RUNNING"`. If you get an empty reply or `404`, the connector has not registered yet — wait and retry, then check `docker-compose logs connect`.

## 5. Send a message (HTTP POST)

Post a schema-valid DENM to geohash `7y0191k4` in the `denm` / `public` group. This body is the project's reference example; it conforms to the DENM ASN.1 schema so it encodes successfully:

```bash
curl -i -X POST http://localhost:5000/api/publish/denm/public/7y0191k4 \
  -H "Content-Type: application/json" \
  -d '{
    "header": { "protocolVersion": 2, "messageID": 1, "stationID": 123456 },
    "denm": {
      "management": {
        "actionID": { "originatingStationID": 123456, "sequenceNumber": 1 },
        "detectionTime": 649940045094,
        "referenceTime": 649940045094,
        "eventPosition": {
          "latitude": 367225309,
          "longitude": -43965883,
          "positionConfidenceEllipse": {
            "semiMajorConfidence": 4095,
            "semiMinorConfidence": 4095,
            "semiMajorOrientation": 3601
          },
          "altitude": { "altitudeValue": 0, "altitudeConfidence": "unavailable" }
        },
        "relevanceDistance": "lessThan500m",
        "validityDuration": 60,
        "stationType": 10
      },
      "situation": {
        "informationQuality": 0,
        "eventType": { "causeCode": 95, "subCauseCode": 0 }
      },
      "location": {
        "eventPositionHeading": { "headingValue": 0, "headingConfidence": 127 },
        "traces": [ [ { "pathPosition": { "deltaLatitude": 2117, "deltaLongitude": 5821, "deltaAltitude": 0 } } ] ]
      }
    }
  }'
```

The service adds 0.5–1.5 s of jitter per request, so the response is not instant. Expected response:

```
HTTP/1.1 200 OK
...
{"key":"v2x/denm/public/g8/7/y/0/1/9/1/k/4","message":"Message processed successfully","sub_service":"DENM","topic":"v2x.denm.public"}
```

The `key` in the response is exactly the MQTT topic the message will appear on.

## 6. Read the message from MQTT

In a **separate** terminal, subscribe to the geohash subtree **before** (or while) re-posting. `-v` prints `topic payload`:

```bash
export MQTT_USER=instantx     # placeholder; ignored by the anonymous broker today
export MQTT_PASS=instantx
mosquitto_sub \
  -h localhost \
  -p 1883 \
  -u "$MQTT_USER" \
  -P "$MQTT_PASS" \
  -i "instantx-http-sub-$(hostname)-$RANDOM" \
  -t "v2x/denm/public/g8/#" \
  -v
```

With the subscriber running, re-run the [section 5](#5-send-a-message-http-post) POST from another terminal. The subscriber prints the topic followed by the UPER payload as a hex string, for example:

```
v2x/denm/public/g8/7/y/0/1/9/1/k/4 02010001e240c50000f120000092ea6e41a4c4ba9b906934...
```

(The exact hex depends on the payload.) Seeing the line confirms the full HTTP → Kafka → MQTT path works. Press `Ctrl+C` to stop the subscriber.

## 7. Input validation reference

The API validates every path segment and the body before encoding. These calls return `400` (or `413`) and never reach Kafka — useful for confirming the API rejects bad input:

| Command (abbreviated) | Response |
|---|---|
| `POST /api/publish/unknown/public/7y0191k4` | `400 {"error":"unsupported sub_service"}` |
| `POST /api/publish/denm/bad.group/7y0191k4` | `400 {"error":"invalid sub_service_group"}` |
| `POST /api/publish/denm/public/ailo` | `400 {"error":"invalid geohash"}` (a, i, l, o are not in the geohash alphabet) |
| body `[1,2,3]` | `400 {"error":"request body must be a JSON object"}` |
| body that does not match the DENM schema (e.g. `{"a":1}`) | `400 {"error":"payload does not conform to the message schema"}` |
| body larger than 1 MiB | `413 Payload Too Large` |

Example (invalid geohash):

```bash
curl -i -X POST http://localhost:5000/api/publish/denm/public/ailo \
  -H "Content-Type: application/json" \
  -d '{"a": 1}'
```

## 8. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `curl: (7) Failed to connect to localhost port 5000` | `api-service` is down or the port is not published. Re-run [section 4](#4-start--verify-the-stack) and check `docker-compose logs api-service`. |
| `400 {"error":"payload does not conform to the message schema"}` | The JSON body is not a valid DENM. Use the exact body from [section 5](#5-send-a-message-http-post). |
| POST returns `200` but nothing appears on MQTT | The MQTT Sink connector is not `RUNNING`, or you subscribed to the wrong topic. Check `curl http://localhost:8083/connectors/MQTTSinkConnector/status` and subscribe to `v2x/denm/public/g8/#`. |
| Connector status is empty / `404` | Kafka Connect has not registered the connector yet (~100 s after start) or it failed — see `docker-compose logs connect`. |
| MQTT payload looks like gibberish | It is the UPER-encoded DENM as a hex string — expected. It is not meant to be human-readable JSON; see [UPER Encoding](./Encoding.md). |

## Related

- [Manual MQTT Testing](./MQTT-Manual-Testing.md) — raw MQTT pub/sub and broker connection details.
- [MQTT Topic Structure](./MQTT-Topic-Structure.md) — how the geohash topic tree is built.
- [Event Publisher](./Event-Publisher.md) — the service's configuration and how to run it locally.
- [UPER Encoding](./Encoding.md) — what the hex payload contains.

## Next step

Decoding the UPER hex payload back into a readable DENM (round-trip verification) and securing the API/broker with TLS are follow-ups to this guide.
