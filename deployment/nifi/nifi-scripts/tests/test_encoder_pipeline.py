import os

import src.encoder_decoder as sut

# ASN.1 schemas live at deployment/nifi/asn, two levels up from this test file.
ASN_FOLDER = os.path.join(os.path.dirname(__file__), "..", "..", "asn")

DENM_XML = "<DenmEtsi><gbcGacHeader><basicHeader><version>1</version><nextHeader>1</nextHeader><reserved>0</reserved><lifeTime><multiplier>19</multiplier><base>0</base></lifeTime><remaingHop>1</remaingHop></basicHeader><commonHeader><nextHeader>2</nextHeader><reserved1>0</reserved1><headerType>4</headerType><headerSubType>0</headerSubType><traficClass><scf><false/></scf><channelOffload><false/></channelOffload><tcID>0</tcID></traficClass><flags><mobile><true/></mobile><reserved>0</reserved></flags><payloadLength>0</payloadLength><maxHopLimit>1</maxHopLimit><reserved2>0</reserved2></commonHeader><sequenceNumber>123</sequenceNumber><reserved1>0</reserved1><sopv><address><configuration><manual/></configuration><stationType>3</stationType><reserved>0</reserved><mid><lsb>0</lsb><msb>0</msb></mid></address><tst>3588788757</tst><latitude>436640930</latitude><longitude>69321627</longitude><pai><false/></pai><speed>-16370</speed><heading>14</heading></sopv><geoArea><lat>436640930</lat><long>69321627</long><distanceA>10</distanceA><distanceB>0</distanceB><angle>0</angle></geoArea><reserved2>0</reserved2></gbcGacHeader><btpb><destinationPort>2002</destinationPort><destinationPortInfo>0</destinationPortInfo></btpb><denm><header><protocolVersion>2</protocolVersion><messageID>1</messageID><stationID>123456789</stationID></header><denm><management><actionID><originatingStationID>123456789</originatingStationID><sequenceNumber>123</sequenceNumber></actionID><detectionTime>1071308466183</detectionTime><referenceTime>1071279612183</referenceTime><eventPosition><latitude>436640930</latitude><longitude>69321627</longitude><positionConfidenceEllipse><semiMajorConfidence>377</semiMajorConfidence><semiMinorConfidence>377</semiMinorConfidence><semiMajorOrientation>0</semiMajorOrientation></positionConfidenceEllipse><altitude><altitudeValue>1200</altitudeValue><altitudeConfidence><alt-000-02/></altitudeConfidence></altitude></eventPosition><relevanceDistance><lessThan50m/></relevanceDistance><relevanceTrafficDirection><allTrafficDirections/></relevanceTrafficDirection><validityDuration>86400</validityDuration><transmissionInterval>500</transmissionInterval><stationType>3</stationType></management><situation><informationQuality>3</informationQuality><eventType><causeCode>2</causeCode><subCauseCode>0</subCauseCode></eventType><linkedCause><causeCode>14</causeCode><subCauseCode>0</subCauseCode></linkedCause><eventHistory><EventPoint><eventPosition><deltaLatitude>0</deltaLatitude><deltaLongitude>20</deltaLongitude><deltaAltitude>0</deltaAltitude></eventPosition><eventDeltaTime>1706733817</eventDeltaTime><informationQuality>1</informationQuality></EventPoint><EventPoint><eventPosition><deltaLatitude>897</deltaLatitude><deltaLongitude>10</deltaLongitude><deltaAltitude>-123</deltaAltitude></eventPosition><informationQuality>2</informationQuality></EventPoint></eventHistory></situation><location><eventSpeed><speedValue>1300</speedValue><speedConfidence>127</speedConfidence></eventSpeed><eventPositionHeading><headingValue>14</headingValue><headingConfidence>127</headingConfidence></eventPositionHeading><traces><PathHistory><PathPoint><pathPosition><deltaLatitude>0</deltaLatitude><deltaLongitude>0</deltaLongitude><deltaAltitude>12800</deltaAltitude></pathPosition><pathDeltaTime>1706733917</pathDeltaTime></PathPoint><PathPoint><pathPosition><deltaLatitude>-123</deltaLatitude><deltaLongitude>987</deltaLongitude><deltaAltitude>20</deltaAltitude></pathPosition></PathPoint></PathHistory></traces></location></denm></denm></DenmEtsi>"  # noqa: E501


def test_transform_xml_normalizes_payload():
    data_dict = sut.transform_xml(DENM_XML, "DenmEtsi")
    # Top-level element removed; the three DenmEtsi parts are present.
    assert "gbcGacHeader" in data_dict
    assert "btpb" in data_dict
    assert "denm" in data_dict


def test_build_encoder_and_encode_denm_etsi():
    data_dict = sut.transform_xml(DENM_XML, "DenmEtsi")
    encoder = sut.build_encoder(ASN_FOLDER)
    encoded = sut.encode_denm_etsi(data_dict, encoder)
    assert isinstance(encoded, (bytes, bytearray))
    assert len(encoded) > 0
    # payloadLength must be set to the combined BTP-B + DENM size during encoding.
    assert data_dict["gbcGacHeader"]["commonHeader"]["payloadLength"] > 0
