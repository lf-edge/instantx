[Home](../README.md) > Apache Kafka and Kafka Connect

# Understanding the Role of Kafka and Kafka Connect in InstantX

**Apache Kafka** is a *distributed streaming platform* that excels at handling real-time data at high throughput and low latency. It's ideal for applications that require processing large volumes of data streams, such as IoT data (specifically V2X).

**Kafka Connect** acts as a bridge between Kafka and external systems, simplifying the process of ingesting and delivering data. It provides pre-built connectors for various data sources and sinks, making it easy to integrate Kafka into existing data pipelines.

In **InstantX**, <u>Apache Kafka</u> works as the pipeline connector between the different components, basically the underlying communication system that links each component to every other component. On the other hand, Kafka Connector, with its custom MQTT Source and Sink connectors facilitares the synchronization between Kafka Broker and MQTT Broker.

## Key Concepts and Benefits

- <U>Topics</U>: The fundamental unit of organization in Kafka. Each topic represents a stream of records.
- <U>Producers</U>: Applications that publish messages to Kafka topics.
- <U>Consumers</U>: Applications that subscribe to Kafka topics and process messages.
- <U>Connectors</U>: Plugins that handle the integration between Kafka and external systems.

## Benefits of using Kafka and Kafka Connect

- <U>Scalability</U>: Kafka can handle massive volumes of data and scale horizontally by adding more brokers.
- <U>Fault Tolerancev:</U> Kafka is highly fault-tolerant, ensuring data durability even in the face of hardware failures.
- <U>Real-time Processing</U>: Kafka enables real-time data processing, making it suitable for applications that require low-latency responses.
- <U>Decoupling</U>: Kafka decouples producers and consumers, allowing them to operate independently.
- <U>Integration</U>: Kafka Connect simplifies the integration of Kafka with various data sources and systems.

<br /><br />

# Configuration and Setup

## Apache Kafka Broker Configuration

Always refer to the oficial [Apache Kafka documentation](https://kafka.apache.org/documentation/) for reference and additional details, or to [Kafka configuration](https://kafka.apache.org/documentation/#configuration).

The current supported release is based on current [Apache Kafka (3.8.0)](https://hub.docker.com/r/apache/kafka)

The provided configuration assumes the use of **KRaft** (*Kafka Raft Metadata mode*) replacing the need for **Apache Zookeeper**. Nonetheless, the current version of Apache Kafka used (*v3.8.0*) still supports Zookeeper and configurations can be changed accordingly, but it is expected that it will be completely ~~removed~~ from Kafka at the next major release (*4.0.0*).

This configuration doesn't include **SSL/TLS** configurations as well as other security (authentication/authorization) and hardening configurations, or multi-node cluster topology. It is up to the user to change those configurations according to each owns needs.

It's also important to note that if you are overriding any Kafka configuration, then none of the default configurations will be used.

Main environment variables used:

- node.id: A unique identifier for the node/broker.
- process.roles: The roles the node is assuming (Broker, Controller) - relevant if Zookeeper is **not** used
- listeners: Specifies the network interface and port for the broker to listen on.
- transaction.state.logs: set to 1 due to a single node being used.
- num.partitions: The maximum retention time for messages in a topic.

```Console
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://:19092,PLAINTEXT_HOST://:9092,CONTROLLER://localhost:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:19092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_NUM_PARTITIONS: 3      
```

<br/><br/>

## Kafka Connect Configuration

Always refer to the oficial [Kafka Connect documentation](https://kafka.apache.org/documentation.html#connect) for reference and additional details.

Main environment variables used:

- bootstrap servers: Apache Kafka endpoint(s).
- rest port: specifies which port is used by Kafka Connect to expose its API(s).
- group id: used by the connectors to establish a consumer with Apache Kafka.
- storage topic(s): topic names used internally by Kafka Connect for management purposes.
- key and value converters: conversion classes used internally to handle Kafka key and value elements
  - Should be changed accordingly with needs.
- plugin path: directly linked to the volume used, to specify to Kafka Connect where to search for additional connectors (source/sink)

```Console
    # Environment variables
    environment:
      CONNECT_BOOTSTRAP_SERVERS: SASL_PLAINTEXT://kafka:19092
      CONNECT_REST_PORT: 8083
      CONNECT_GROUP_ID: kafka-connect
      CONNECT_CONFIG_STORAGE_TOPIC: kc_connect-configs
      CONNECT_OFFSET_STORAGE_TOPIC: kc_connect-offsets
      CONNECT_STATUS_STORAGE_TOPIC: kc_connect-status
      CONNECT_KEY_CONVERTER: org.apache.kafka.connect.storage.StringConverter
      CONNECT_VALUE_CONVERTER: org.apache.kafka.connect.storage.StringConverter
      CONNECT_KEY_CONVERTER_SCHEMAS_ENABLE: false
      CONNECT_VALUE_CONVERTER_SCHEMAS_ENABLE: false
      CONNECT_INTERNAL_KEY_CONVERTER: org.apache.kafka.connect.storage.StringConverter
      CONNECT_INTERNAL_VALUE_CONVERTER: org.apache.kafka.connect.storage.StringConverter
      #CONNECT_REST_ADVERTISED_HOST_NAME: connect
      CONNECT_REST_ADVERTISED_HOST_NAME: localhost
      CONNECT_LOG4J_ROOT_LOGLEVEL: "INFO"
      CONNECT_LOG4J_LOGGERS: "org.apache.kafka.connect.runtime.rest=WARN,org.reflections=ERROR"
      CONNECT_LOG4J_APPENDER_STDOUT_LAYOUT_CONVERSIONPATTERN: "[%d] %p %X{connector.context}%m (%c:%L)%n"
      CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR: "1"
      CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR: "1"
      CONNECT_STATUS_STORAGE_REPLICATION_FACTOR: "1"
      CONNECT_PLUGIN_PATH: '/etc/kafka-connect/jars,/usr/share/java/'
    # Volumes - loads the pre-defined custom MQTT Source and Sink connectors (jar) into Kafka connect on startup
    volumes:
      - ./kafka-connect:/etc/kafka-connect/jars
```

This InstantX release contains two custom connectors which support **MQTT Source and Sink** operations.
They are mainly used to <u>synchronize messages from MQTT to Kafka broker and vice-versa</u>. This synchronization doesn't apply any transformation or modification to the message payload, but transforms the topic structure from the [MQTT geohash based structure](./MQTT-Topic-Structure.md) to a more generic Kafka topic structure without the inclusion of the geohash in it. Nonetheless, the original geohash topic structure is used as the Kafka Key on the message conversion.

### Source Connector

The MQTT Source connector starts an MQTT Client and subscribes to the topic(s) defined in the Connector configurations, and sends all received messages to Kafka Broker.

```Json
{
 "name": "MQTTSourceConnector",
 "connector.class": "com.instantx.kafka.connectors.MQTTSourceConnector",
 "tasks.max": 1,
 "key.converter": "org.apache.kafka.connect.storage.StringConverter",
 "value.converter": "org.apache.kafka.connect.converters.ByteArrayConverter", 
 "mqtt.broker": "tcp://mqtt:1883",
 "mqtt.clientID": "clientSource",
 "mqtt.topic": "v2x/cam/public/g8/+/+/+/+/#",
 "mqtt.qos": 1,
 "mqtt.automaticReconnect": true,
 "mqtt.keepAliveInterval": 10000,
 "mqtt.cleanSession": true,
 "mqtt.connectionTimeout": 1000,
 "mqtt.connector.auth": false,
 "mqtt.connector.auth.userName": "",
 "mqtt.connector.auth.password": "",
 "mqtt.connector.ssl": false,
 "mqtt.connector.ssl.ca": ""
}
```

### Sink Connector

The MQTT Sink Connector, subscribes to the Kafka topic(s) defined by the configured topic pattern (*topics.regex*), and sends all received traffic to the MQTT Broker through the MQTT client. An additional feature of this Sink connector, is the use of a message buffer to collect received messages instead of triggering an automatic MQTT publishing for each individual message received. This buffer can be enabled/disabled (*buffer.enable*) based on the defined configurations, as well as the buffer size (*buffer.size*) and frequency in which is it flushed (*buffer.flush.frequency*).

```Json
{
 "name": "MQTTSinkConnector",
 "connector.class": "com.instantx.kafka.connectors.MQTTSinkConnector",
 "tasks.max": 1,
 "topics.regex": "v2x\\.(cam|denm)\\.*",
 "mqtt.broker": "tcp://mqtt:1883",
 "mqtt.clientID": "clientSink",
 "mqtt.qos": "1",
 "mqtt.automaticReconnect": true,
 "mqtt.keepAliveInterval": 10000,
 "mqtt.cleanSession": true,
 "mqtt.connectionTimeout": 1000,
 "mqtt.connector.auth": false,
 "mqtt.connector.auth.userName": "",
 "mqtt.connector.auth.password": "",
 "mqtt.connector.ssl": false,
 "mqtt.connector.ssl.ca": "",
 "buffer.enable": false,
 "buffer.size": 100,
 "buffer.flush.frequency": 1000
}
```

### Kafka Connect API(s)

Upon starting Kafka Connect, these custom connectors are available for use, but not actually instanciated.
To accomplish this, the user will need to call Kafka Connect API (*Create Connector*) providing the new connector name, as well as the desired configurations.

**POST** =={{kafka-connect.server}}:{{kafka-connect.port}}/connectors==

```Json
{
    "name": "{fill in with desired source connector name}",
    "config": {
        "...source connector configurations as seen in the Json example above...."
    }
}
```

<br/>
and/or
<br/>

```Json
{
    "name": "{fill in with desired sink connector name}",
    "config": {
        "...sink connector configurations as seen in the Json example above...."
    }
}
```
