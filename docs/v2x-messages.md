[Home](../README.md) > ETSI C-ITS Messages

# V2X Standard messages

## Introduction

**ETSI** ([European Telecommunications Standards Institute](https://www.etsi.org/)) **C-ITS** ([Cooperative Intelligent Transport Systems](https://portal.etsi.org/Services/Centre-for-Testing-Interoperability/Activities/Intelligent-Transport-System/C-ITS-Protocols)) play a pivotal role in revolutionizing transportation systems by enabling vehicles and infrastructure to communicate with each other. These systems enhance road safety, optimize traffic flow, and improve overall efficiency on the roads.

This document delves into the specifics of two crucial message formats defined by ETSI for C-ITS: **DENM v2** ([Decentralized Environmental Notification Message](https://www.etsi.org/deliver/etsi_en/302600_302699/30263703/01.03.01_60/en_30263703v010301p.pdf)) and **IVIM** ([Infrastructure to Vehicle Information Message](https://www.etsi.org/deliver/etsi_ts/103300_103399/103301/02.01.01_60/ts_103301v020101p.pdf)). 


## ETSI C-ITS Messages


| C-ITS Message Type | ETSI Standard |
| --------- | ---------- |
| DENM (v2) | [ETSI EN 302 637-3 V1.3.1 (2019-04)](https://www.etsi.org/deliver/etsi_en/302600_302699/30263703/01.03.01_60/en_30263703v010301p.pdf) |
| IVIM | [ETSI TS 103 301 V2.1.1 (2021-03)](https://www.etsi.org/deliver/etsi_ts/103300_103399/103301/02.01.01_60/ts_103301v020101p.pdf) |

### DENM (Decentralized Environmental Notification Message)

**DENM** is a message format that provides notifications about events or hazards detected by vehicles or infrastructure, that can impact road safety.
The information included in a DENM can vary depending on the type of hazard or event being reported, but typically includes information such as:

- Event type (e.g., road works, accidents, hazards, weather conditions, emergency vehicles, etc..)
- Location and size of the event
- Time and duration of the event
- Additional details

### IVIM (Infrastructure to Vehicle Information Message)

**IVIM** is another message format that facilitate real-time data sharing among vehicles and with roadside infrastructure to enhance safety and traffic efficiency. If provides information such as:

- Roadside information (e.g., traffic signs, speed limits)
- Road conditions
- Parking availability
- Traffic conditions
- and other types of data that can enhance the driver’s experience

## Package Structure

Each exchanged C-ITS message is expected to be included in a packet containing a **GeoNetworking header** ([GN](https://www.etsi.org/deliver/etsi_en/302600_302699/3026360401/01.04.01_60/en_3026360401v010401p.pdf)) and a **BTP-B header** ([Basic Transport Protocol](https://www.etsi.org/deliver/etsi_EN/302600_302699/3026360501/02.02.01_60/en_3026360501v020201p.pdf)).

| GN Header | BTP Header | C-ITS Message |
| --------- | ---------- | -------------- |
| ETSI EN 302 636-4-1 V1.4.1 (2020-01) | ETSI EN 302 636-5-1 V2.2.1 (2019-05) | *DENM,IVIM,... included in the packet shall be [ASN.1 UPER encoded.](./Encoding.md)* |
 

### 1. GeoNetwork Header

The GeoNetwork Header contains metadata related to the geographic scope and routing of the message. It includes information such as:

- **Geographic Region**: Specifies the geographical area covered by the message.
  
- **Validity Period**: Defines the time window during which the message is considered valid and relevant.
  
- **Security Information**: Includes cryptographic signatures or other security measures to ensure message authenticity and integrity. 

> *The Security Header included in the GN Header is not required.*
 
 
### 2. BTP-B (Basic Transport Protocol Block) Header

The BTPB Header provides basic transport-level information necessary for routing and handling the message within the communication network. It includes:

- **Destination Port**: It identifies the protocol entity at the ITS facilities layer in the destination. For well-known ports it shall be set to a value corresponding to the identified facilities layer service as specified the values in [ETSI TS 103 248](https://www.etsi.org/deliver/etsi_ts/103200_103299/103248/02.01.01_60/ts_103248v020101p.pdf). 

- **Destination Port Info**: It provides additional information. Default setting is 0.



