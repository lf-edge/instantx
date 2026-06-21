[Home](../README.md) > Manual MQTT Testing

# Manual MQTT Testing

This guide shows how to manually validate the InstantX MQTT publish/subscribe flow against the local broker (HiveMQ CE running in Docker) using the `mosquitto` command-line clients. You should be able to install the tools, connect, and watch a message travel from a publisher to a subscriber in under five minutes.

> The broker is the [HiveMQ Community Edition] image started by the `docker-compose` stack (service `mqtt`). You do **not** need to install a broker locally — only the client tools.

## 1. Prerequisites

Install the `mosquitto` clients (`mosquitto_pub` / `mosquitto_sub`). You only need the **clients**, not the broker: the broker already runs in Docker.

| Platform | Command |
|---|---|
| macOS (Homebrew) | `brew install mosquitto` |
| Debian / Ubuntu | `sudo apt install mosquitto-clients` |
| Windows (winget) | `winget install EclipseFoundation.Mosquitto` |

On macOS, `brew install mosquitto` installs both the broker and the clients; you can ignore the broker. On Windows you can also use the installer from [mosquitto.org/download](https://mosquitto.org/download/) and add its `bin` directory to your `PATH`.

Verify the clients are available:

```bash
mosquitto_pub --help
mosquitto_sub --help
```

## 2. Connection variables

| Variable | Value | Notes |
|---|---|---|
| Host | `localhost` | From your host machine. From another container on the stack network, use the service name `mqtt`. |
| Port | `1883` | Plain MQTT, published by the `mqtt` service in `deployment/docker-compose.yml`. |
| Username | _(none by default)_ | The default stack runs HiveMQ CE with anonymous access — no credentials required. See note below. |
| Password | _(none by default)_ | Same as above. |
| Topic | `v2x/denm/public/g8/7/y/0/1/9/1/k/4` | See [MQTT Topic Structure](./MQTT-Topic-Structure.md). |
| Client ID | `instantx-<role>-<unique>` | Must be unique per connection (see [Important notes](#7-important-notes)). |

**Credentials.** The committed stack does not enable broker authentication (the MQTT connectors set `mqtt.connector.auth: "false"`), so any username / password you pass is accepted but unused. To keep the commands below copy-pasteable and ready for a future auth-enabled broker, export them as environment variables instead of hard-coding secrets:

```bash
export MQTT_USER=instantx     # placeholder; ignored by the anonymous broker today
export MQTT_PASS=instantx     # placeholder; replace once auth is enabled
```

> Never commit real credentials to the repository or paste them into docs. Once the broker enforces authentication, credentials are supplied at runtime via environment variables / git-ignored `.env` files (see [Security Architecture](./Security-Architecture.md)).

## 3. Start / verify the broker in Docker

From `deployment/`, make sure the broker container is running and port 1883 is published:

```bash
cd deployment
docker-compose up -d mqtt        # start just the broker (or `docker-compose up -d` for the full stack)
docker-compose ps mqtt           # STATE should be "running" / "Up"
```

Confirm the port mapping (`0.0.0.0:1883->1883/tcp`):

```bash
docker ps --filter "name=instantx_mqtt" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Expected output (truncated):

```
NAMES            STATUS         PORTS
instantx_mqtt    Up 10 seconds  0.0.0.0:1883->1883/tcp, ...
```

## 4. Subscriber (consumer)

In one terminal, subscribe to the test topic. `-v` prints `topic payload` so you can see which topic each message arrived on:

```bash
mosquitto_sub \
  -h localhost \
  -p 1883 \
  -u "$MQTT_USER" \
  -P "$MQTT_PASS" \
  -i "instantx-sub-$(hostname)-$RANDOM" \
  -t "v2x/denm/public/g8/#" \
  -v
```

The command blocks and waits for messages. The `#` wildcard matches every geohash under `v2x/denm/public/g8/`.

## 5. Publisher (producer)

In a **second** terminal, publish a message to a concrete topic under that subtree:

```bash
mosquitto_pub \
  -h localhost \
  -p 1883 \
  -u "$MQTT_USER" \
  -P "$MQTT_PASS" \
  -i "instantx-pub-$(hostname)-$RANDOM" \
  -t "v2x/denm/public/g8/7/y/0/1/9/1/k/4" \
  -m '{"test":"hello-instantx"}'
```

`mosquitto_pub` connects, sends the message, and exits.

## 6. Validate the flow

1. Export the connection variables from [section 2](#2-connection-variables) and start the subscriber from [section 4](#4-subscriber-consumer). Leave it running.
2. In a second terminal, export the same variables and run the publisher from [section 5](#5-publisher-producer).
3. Switch back to the subscriber terminal. You should immediately see:

   ```
   v2x/denm/public/g8/7/y/0/1/9/1/k/4 {"test":"hello-instantx"}
   ```

If the line appears, the publish/subscribe flow through the broker works. Press `Ctrl+C` to stop the subscriber.

## 7. Important notes

- **Client IDs must be unique per connection.** The subscriber and publisher cannot share the same `-i` value: MQTT brokers allow only one connection per client ID and will disconnect the older one. Use a randomized pattern, e.g.:

  ```bash
  -i "instantx-sub-$(hostname)-$RANDOM"
  ```

- **Running the clients from another container** on the same Docker network (`nifi_network`): use the service name `mqtt` instead of `localhost`, and the internal port `1883`:

  ```bash
  docker-compose exec connect \
    mosquitto_pub -h mqtt -p 1883 \
      -i "instantx-pub-$RANDOM" \
      -t "v2x/denm/public/g8/7/y/0/1/9/1/k/4" \
      -m '{"test":"hello-instantx"}'
  ```

## 8. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `Connection Refused: not authorised` | The broker now enforces auth and your `-u` / `-P` are wrong or missing. Re-check the credentials supplied to the stack. |
| `Error: Connection refused` (cannot reach host) | Port `1883` is not published, or the broker container is down. Re-run [section 3](#3-start--verify-the-broker-in-docker). |
| Subscriber repeatedly connects / disconnects | The subscriber and publisher share the same client ID (`-i`). Give each a unique ID. |
| `mosquitto_sub: command not found` | The clients are not installed or not on `PATH`. See [section 1](#1-prerequisites). |

## Next step

Secure the connection with TLS over port `8883` (currently **not** enabled in the default stack). Documenting the TLS workflow — broker listener config and client `--cafile` / `--cert` / `--key` flags — is a follow-up to this guide.

[HiveMQ Community Edition]: https://github.com/hivemq/hivemq-community-edition
