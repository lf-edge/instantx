from binascii import hexlify
import os
import asn1tools
import xmltodict

import src.encoder_decoder as sut

# ---------------------------------
# convert_dictionary function tests
# ---------------------------------


def test_should_convert_mixed_data_structures():
    # Given: a complex structure with various convertible types
    data = {
        "bool_str": "True",
        "bool_str_false": "False",
        "bool_dict": {"false": None},
        "single_key": {"hello": None},
        "number": "-12",
        "empty_list": [None],
        "nested": {"inner": {"true": None}},
    }

    # When: the conversion function is applied
    sut.convert_dictionary(data)

    # Then: all fields are converted to their expected native types
    assert data == {
        "bool_str": True,
        "bool_str_false": False,
        "bool_dict": False,
        "single_key": "hello",
        "number": -12,
        "empty_list": [],
        "nested": {"inner": True},
    }


def test_should_convert_list_of_dicts():
    # Given: a list of dictionaries with convertible values
    data = [{"flag": "false"}, {"count": "5"}]

    # When: the conversion function is applied
    sut.convert_dictionary(data)

    # Then: all values are converted appropriately
    assert data == [{"flag": False}, {"count": 5}]


# --------------------------------------
# replace_specific_values function tests
# --------------------------------------


def test_single_dict_with_predefined_key():
    # Given: A dictionary containing a single key "first" nested inside "name"
    data = {"person": {"name": {"first": "John"}}}
    predefined_keys = ["first"]
    special_keys = []

    # When: The function replace_specific_values is called
    sut.replace_specific_values(data, predefined_keys, special_keys)

    # Then: The dictionary under "name" should be replaced with a list containing "John"
    assert data == {"person": {"name": ["John"]}}


def test_multiple_keys_in_nested_dict():
    # Given: A dictionary where "user" contains "profile" with nested "name" and "address" dictionaries
    #         which have keys "first" and "city" (both are in predefined_keys)
    data = {
        "user": {"profile": {"name": {"first": "John"}, "address": {"city": "Madrid"}}}
    }
    predefined_keys = ["first", "city"]
    special_keys = []

    # When: The function replace_specific_values is called
    sut.replace_specific_values(data, predefined_keys, special_keys)

    # Then: Both "first" and "city" values should be replaced by lists containing their respective values
    assert data == {"user": {"profile": {"name": ["John"], "address": ["Madrid"]}}}


# -------------------
# main function tests
# -------------------


def test_main_function_with_valid_input():
    # FIXME: Mock few parts of this test

    # Given: A valid XML string `input_data` and an expected valid path for `DATA_FOLDER`
    input_data = "<DenmEtsi><gbcGacHeader><basicHeader><version>1</version><nextHeader>1</nextHeader><reserved>0</reserved><lifeTime><multiplier>19</multiplier><base>0</base></lifeTime><remaingHop>1</remaingHop></basicHeader><commonHeader><nextHeader>2</nextHeader><reserved1>0</reserved1><headerType>4</headerType><headerSubType>0</headerSubType><traficClass><scf><false/></scf><channelOffload><false/></channelOffload><tcID>0</tcID></traficClass><flags><mobile><true/></mobile><reserved>0</reserved></flags><payloadLength>0</payloadLength><maxHopLimit>1</maxHopLimit><reserved2>0</reserved2></commonHeader><sequenceNumber>123</sequenceNumber><reserved1>0</reserved1><sopv><address><configuration><manual/></configuration><stationType>3</stationType><reserved>0</reserved><mid><lsb>0</lsb><msb>0</msb></mid></address><tst>3588788757</tst><latitude>436640930</latitude><longitude>69321627</longitude><pai><false/></pai><speed>-16370</speed><heading>14</heading></sopv><geoArea><lat>436640930</lat><long>69321627</long><distanceA>10</distanceA><distanceB>0</distanceB><angle>0</angle></geoArea><reserved2>0</reserved2></gbcGacHeader><btpb><destinationPort>2002</destinationPort><destinationPortInfo>0</destinationPortInfo></btpb><denm><header><protocolVersion>2</protocolVersion><messageID>1</messageID><stationID>123456789</stationID></header><denm><management><actionID><originatingStationID>123456789</originatingStationID><sequenceNumber>123</sequenceNumber></actionID><detectionTime>1071308466183</detectionTime><referenceTime>1071279612183</referenceTime><eventPosition><latitude>436640930</latitude><longitude>69321627</longitude><positionConfidenceEllipse><semiMajorConfidence>377</semiMajorConfidence><semiMinorConfidence>377</semiMinorConfidence><semiMajorOrientation>0</semiMajorOrientation></positionConfidenceEllipse><altitude><altitudeValue>1200</altitudeValue><altitudeConfidence><alt-000-02/></altitudeConfidence></altitude></eventPosition><relevanceDistance><lessThan50m/></relevanceDistance><relevanceTrafficDirection><allTrafficDirections/></relevanceTrafficDirection><validityDuration>86400</validityDuration><transmissionInterval>500</transmissionInterval><stationType>3</stationType></management><situation><informationQuality>3</informationQuality><eventType><causeCode>2</causeCode><subCauseCode>0</subCauseCode></eventType><linkedCause><causeCode>14</causeCode><subCauseCode>0</subCauseCode></linkedCause><eventHistory><EventPoint><eventPosition><deltaLatitude>0</deltaLatitude><deltaLongitude>20</deltaLongitude><deltaAltitude>0</deltaAltitude></eventPosition><eventDeltaTime>1706733817</eventDeltaTime><informationQuality>1</informationQuality></EventPoint><EventPoint><eventPosition><deltaLatitude>897</deltaLatitude><deltaLongitude>10</deltaLongitude><deltaAltitude>-123</deltaAltitude></eventPosition><informationQuality>2</informationQuality></EventPoint></eventHistory></situation><location><eventSpeed><speedValue>1300</speedValue><speedConfidence>127</speedConfidence></eventSpeed><eventPositionHeading><headingValue>14</headingValue><headingConfidence>127</headingConfidence></eventPositionHeading><traces><PathHistory><PathPoint><pathPosition><deltaLatitude>0</deltaLatitude><deltaLongitude>0</deltaLongitude><deltaAltitude>12800</deltaAltitude></pathPosition><pathDeltaTime>1706733917</pathDeltaTime></PathPoint><PathPoint><pathPosition><deltaLatitude>-123</deltaLatitude><deltaLongitude>987</deltaLongitude><deltaAltitude>20</deltaAltitude></pathPosition></PathPoint></PathHistory></traces></location></denm></denm></DenmEtsi>"
    message_type = "DenmEtsi"
    DATA_FOLDER = "/Users/luisalfredo.perez/Developer/instantx/internal/instantX-platform/deployment/nifi/asn"

    # When: The main function is executed
    data_dict = xmltodict.parse(input_data, force_list=["traces", "eventHistory"])
    data_dict = data_dict[message_type]
    sut.convert_dictionary(data_dict)
    sut.replace_specific_values(data_dict, [], ["EventPoint"])
    sut.replace_specific_values(data_dict, ["PathHistory"], [])
    sut.replace_specific_values(data_dict, ["PathPoint"], [])

    # Find .asn files in the folder
    asn1_files = [
        os.path.join(DATA_FOLDER, f)
        for f in os.listdir(DATA_FOLDER)
        if f.endswith(".asn")
    ]
    encoder = asn1tools.compile_files(
        asn1_files,
        codec="uper",
        any_defined_by_choices=None,
        encoding="utf-8",
        numeric_enums=False,
    )
    encoded = encoder.encode(message_type, data_dict)
    message = hexlify(encoded).decode("ascii")

    # Then: The output message should be a non-empty hex string
    assert isinstance(message, str)
    assert len(message) > 0
