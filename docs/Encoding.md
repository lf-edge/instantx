[Home](../README.md) > UPER Encoding/Decoding

# UPER Encoding/Decoding

UPER (Unaligned Packed Encoding Rules) is a binary encoding format used in C-ITS messages, including DENM and IVIM. It optimizes message size while ensuring efficient encoding and decoding processes.

## How UPER Encoding Works

1. **Data Structure Definition**: Each message type (e.g., DENM, IVIM) defines its data structure using ASN.1 (Abstract Syntax Notation One).

2. **Mapping to ASN.1 Types**: ASN.1 types (e.g., INTEGER, OCTET STRING) are mapped to corresponding data elements in the message structure.

3. **UPER Encoding**: Data elements are encoded using UPER rules, which involve:
   - Breaking down data into smaller components
   - Encoding each component according to predefined rules
   - Packing encoded components into binary format

4. **Bit-Level Optimization**: UPER optimizes the use of individual bits within bytes to minimize message size without sacrificing data integrity.

## How UPER Decoding Works

1. **Binary Input**: The encoded message in binary format is received by the decoder.

2. **UPER Decoding**: The decoder interprets the binary stream according to UPER rules, which involves:
   - Unpacking binary data into individual components
   - Decoding each component based on its predefined rules
   - Reconstructing the original data structure

3. **ASN.1 Mapping**: Decoded components are mapped back to their corresponding ASN.1 types and data elements.

4. **Output**: The decoded message is then available for further processing or display within C-ITS applications.

UPER encoding and decoding ensure efficient and reliable communication of C-ITS messages while minimizing bandwidth usage and processing overhead.

## Examples

### Encoded DENM Message Payload (hexadecimal representation)

`11004c01204000800050010003db00009400000000000000adbed407f974b8e6f952f45d000d000e7974b8e67952f45d000a00000000000007d200000201012fd537c78097ea9b81ed9f2d8fa1a3c7cb63e868f2f19a1e6649cc65d17917900018b5010546001f3056c1c0061000dff8480e018d841196eac3e4a01c780c518d3261453f0077e000`

### Json representation of the same message

```json
{
  "gbcGacHeader":{
    "basicHeader":{
      "version":1,
      "nextHeader":1,
      "reserved":0,
      "lifeTime":{
        "multiplier":19,
        "base":0
      },
      "remaingHop":1
    },
    "commonHeader":{
      "nextHeader":2,
      "reserved1":0,
      "headerType":4,
      "headerSubType":0,
      "traficClass":{
        "scf":false,
        "channelOffload":false,
        "tcID":0
      },
      "flags":{
        "mobile":true,
        "reserved":0
      },
      "payloadLength":80,
      "maxHopLimit":1,
      "reserved2":0
    },
    "sequenceNumber":987,
    "reserved1":0,
    "sopv":{
      "address":{
        "configuration":"manual",
        "stationType":5,
        "reserved":0,
        "mid":{
          "lsb":0,
          "msb":0
        }
      },
      "tst":2914964487,
      "latitude":2037692646,
      "longitude":2035479645,
      "pai":false,
      "speed":-16370,
      "heading":14
    },
    "geoArea":{
      "lat":-109791002,
      "long":-112004003,
      "distanceA":10,
      "distanceB":0,
      "angle":0
    },
    "reserved2":0
  },
  "btpb":{
    "destinationPort":2002,
    "destinationPortInfo":0
  },
  "denm":{
    "header":{
      "protocolVersion":2,
      "messageID":1,
      "stationID":19911991
    },
    "denm":{
      "management":{
        "actionID":{
          "originatingStationID":19911991,
          "sequenceNumber":987
        },
        "detectionTime":1071266991390,
        "referenceTime":1071266991390,
        "eventPosition":{
          "latitude":-109791002,
          "longitude":-112004003,
          "positionConfidenceEllipse":{
            "semiMajorConfidence":377,
            "semiMinorConfidence":377,
            "semiMajorOrientation":0
          },
          "altitude":{
            "altitudeValue":1200,
            "altitudeConfidence":"alt-000-02"
          }
        },
        "relevanceDistance":"lessThan50m",
        "relevanceTrafficDirection":"allTrafficDirections",
        "validityDuration":86400,
        "transmissionInterval":500,
        "stationType":5
      },
      "situation":{
        "informationQuality":3,
        "eventType":{
          "causeCode":14,
          "subCauseCode":0
        },
        "linkedCause":{
          "causeCode":97,
          "subCauseCode":0
        },
        "eventHistory":[
          {
            "eventPosition":{
              "deltaLatitude":-123,
              "deltaLongitude":897,
              "deltaAltitude":20
            },
            "eventDeltaTime":1706733817,
            "informationQuality":1
          },
          {
            "eventPosition":{
              "deltaLatitude":456,
              "deltaLongitude":789,
              "deltaAltitude":10
            },
            "informationQuality":2
          }
        ]
      },
      "location":{
        "eventSpeed":{
          "speedValue":1300,
          "speedConfidence":127
        },
        "eventPositionHeading":{
          "headingValue":14,
          "headingConfidence":127
        },
        "traces":[
          [
             
          ]
        ]
      }
    }
  }
}
```

### Wireshark export of the same message

```console
Intelligent Transport Systems
    ItsPduHeader
        protocolVersion: 2
        messageID: denm (1)
        stationID: 19911991
    DecentralizedEnvironmentalNotificationMessage
        management
            actionID
                originatingStationID: 19911991
                sequenceNumber: 987
            detectionTime: 2037-12-11 22:09:46.390 (1071266991390)
            referenceTime: 2037-12-11 22:09:46.390 (1071266991390)
            eventPosition
                latitude: 10°58'44.761"S (-109791002)
                longitude: 11°12'1.441"W (-112004003)
                positionConfidenceEllipse
                    semiMajorConfidence: 3.77m (377)
                    semiMinorConfidence: 3.77m (377)
                    semiMajorOrientation: wgs84North (0)
                altitude
                    altitudeValue: 12.00m (1200)
                    altitudeConfidence: alt-000-02 (1)
            relevanceDistance: lessThan50m (0)
            relevanceTrafficDirection: allTrafficDirections (0)
            validityDuration: 24:00:00 (86400)
            transmissionInterval: Unknown (500)
            stationType: passengerCar (5)
        situation
            informationQuality: Unknown (3)
            eventType
                causeCode: wrongWayDriving (14)
                wrongWayDrivingSubCauseCode: unavailable (0)
            linkedCause
                causeCode: collisionRisk (97)
                collisionRiskSubCauseCode: unavailable (0)
            eventHistory: 2 items
                Item 0
                    EventPoint
                        eventPosition
                            deltaLatitude: 0°0'0.044"S (-123)
                            deltaLongitude: 0°0'0.323"E (897)
                            deltaAltitude: 0.20m (20)
                        eventDeltaTime: 17067338.17s (1706733817)
                        informationQuality: lowest (1)
                Item 1
                    EventPoint
                        eventPosition
                            deltaLatitude: 0°0'0.164"N (456)
                            deltaLongitude: 0°0'0.284"E (789)
                            deltaAltitude: 0.10m (10)
                        informationQuality: Unknown (2)
        location
            eventSpeed
                speedValue: 13.00m/s = 46.8km/h (1300)
                speedConfidence: unavailable (127)
            eventPositionHeading
                headingValue: 1.4° (14)
                headingConfidence: unavailable (127)
            traces: 1 item
```

