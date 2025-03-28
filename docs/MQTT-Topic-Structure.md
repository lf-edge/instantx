[Home](../README.md) > MQTT Topic Structure

# MQTT Topic Structure

In IoT applications, utilizing [geohash-based MQTT topic structures](Geohashes.md) can facilitate efficient communication and management of spatial data. Here's how you can leverage such a structure effectively.

## Topic Structure Overview

The topic structure can be divided into 2 distinct sections:
- <u>*Message related section*</u> = `{service}/{subService}/{subServiceGroup}/`
- <u>*Location related section*</u> = `{geohashLevel}/{geohashes}`

### Example Topic Structure

Let's consider an example geohash-based MQTT topic structure:

`v2x/denm/public/g8/7/y/0/1/9/1/k/4`


In this structure:

- **Level 1 (`service`)**: Denotes the top-level category, identifying the main category to which the message type belongs (e.g. v2x for standard ETSI C-ITS messages).

- **Level 2 (`subService`)**: Identifies the message type (e.g. DENM, IVIM, but it can also include custom types).

- **Level 3 (`subService group`)**: It is used to identify the visibility of the message (e.g. "public" / or a different string for private topics).

- **Level 4 (`geohash level`)**: Denotes the top-level category, indicating that the topic structure is based on geohashes.

- **Level 5..12 (`geohash`)**: Geohash prefix that denotes which geohash level was used (e.g. g8, g7, g6, ...)

- **Level 2 (`region1`, `region2`, `region3`, etc.)**: Represents different levels of geohash precision, allowing for regions of varying sizes. Each subsequent level provides finer spatial granularity.


## Using the Topic Structure

### Subscribing to Topics

Subscribing to specific regions within the geohash-based topic structure can be achieved using wildcard characters:

- **Single-level Wildcard (+)**: Matches any single level in the hierarchy. This allows subscribing to specific regions at a certain level of granularity.
  - Example: `v2x/denm/public/g8/q/s/t/2/e/z/+/+` subscribes to all denm public g8 messages within the `qst2ez` geohash area.
- Example: `v2x/+/public/g8/q/s/t/2/e/z/+/+` subscribes to all public g8 message types within the g4 `qst2` geohash area.
- **Multi-level Wildcard (#)**: Matches any number of levels, enabling subscription to regions at various granularities.
  - Example: `v2x/denm/public/g8/q/s/t/2/e/z/#` similar to the 1st example, subscribes to all g8 messages within the `qst2ez` geohash area, regardless of the level of granularity.

### Publishing Messages

When publishing messages, clients should adhere to the defined geohash-based topic structure to ensure proper routing and organization:

- Example Topic: `Service/SubService/SubService Group/geohash level/level1/level2/level...`
  - Clients publishing to this topic should provide relevant data or commands related to the specified region.

## Conclusion

Utilizing a geohash-based MQTT topic structure allows for efficient communication and management of spatial data in IoT applications. By subscribing to and publishing messages within specific regions of varying sizes, IoT systems can effectively handle spatially distributed information.

