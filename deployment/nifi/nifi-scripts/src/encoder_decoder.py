# ========================LICENSE_START=================================
# Event Publisher
# %%
# Copyright (C) 2024 - 2025 Vodafone
# %%
# Licensed under the MIT License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://opensource.org/license/mit
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================LICENSE_END==================================

import sys
import asn1tools
import os
import xmltodict
from binascii import hexlify
from typing import Any, Dict, List, Union


def convert_dictionary(data: Union[dict, list]) -> None:
    """
    Recursively converts values in a dictionary or list of dictionaries to
    more appropriate Python native types.
    Transformations:

    - Strings 'True'/'true' → Boolean `True`
    - Strings 'False'/'false' → Boolean `False`
    - Dicts {'true': None} → Boolean `True`
    - Dicts {'false': None} → Boolean `False`
    - Dicts with one key and value None → The single key as string
    - Numeric strings → Integers
    - Lists with a single `None` element → Empty list
    - Applies recursively to nested dicts and lists
    Parameters:

    - data (Union[dict, list]): A dictionary or list to process. The function
    modifies the input in-place.
    Returns:

    - None
    """
    if isinstance(data, dict):
        # Iterate through each key-value pair in the dictionary
        for key, value in list(data.items()):
            # Convert 'True'/'true' strings to boolean True
            if value in ["True", "true"]:
                data[key] = True
            # Convert dict {'true': None} to boolean True
            elif isinstance(value, dict) and "true" in value and value["true"] is None:
                data[key] = True
            # Convert 'False'/'false' strings to boolean False
            elif value in ["False", "false"]:
                data[key] = False
            # Convert dict {'false': None} to boolean False
            elif (
                isinstance(value, dict) and "false" in value and value["false"] is None
            ):
                data[key] = False
            # Convert single-key dictionaries like {'something': None} to their key
            elif (
                isinstance(value, dict)
                and len(value) == 1
                and list(value.values())[0] is None
            ):
                data[key] = list(value.keys())[0]
            # Convert numeric strings (like '42', '-3') to integers
            elif isinstance(value, str) and (
                value.isdigit() or (value.startswith("-") and value[1:].isdigit())
            ):
                data[key] = int(value)
            # Convert lists with a single None element to an empty list
            elif isinstance(value, list) and value == [None]:
                data[key] = []
            else:
                # Recurse if the value is not one of the above
                convert_dictionary(value)
    # If the data is a list, recursively process each item
    elif isinstance(data, list):
        for item in data:
            convert_dictionary(item)


def replace_specific_values(
    data: Union[Dict[str, Any], List[Any]],
    predefined_keys: List[str],
    special_keys: List[str],
) -> None:
    """
    Recursively traverses a nested dictionary or list and replaces specific
    nested structures with simplified lists of values, based on a set of predefined keys.

    This function looks for two specific patterns:
    1. A dictionary with a single key from `predefined_keys` and replaces it with a list
      containing the corresponding value.
      Example: { "key": { "target": "value" } } → { "key": ["value"] }

    2. A list containing a single dictionary with a single key from `predefined_keys`,
      and replaces it with a list containing the corresponding value.
      Example: { "key": [ { "target": "value" } ] } → { "key": ["value"] }

    Args:
        data (dict | list): The input data structure (can be nested) to be processed.
        predefined_keys (list[str]): A list of keys to match against when identifying patterns to transform.

    Returns:
        None: The function modifies the `data` object in place.
    """
    # Check if data is a dictionary
    if isinstance(data, dict):
        # Iterate over each key-value pair in the dictionary
        for key, value in data.items():
            # Check if value is a dict with exactly one key and that key is in predefined_keys
            if (
                isinstance(value, dict)
                and len(value) == 1  # The dict has exactly one key
                and list(value.keys())[0] in predefined_keys
            ):  # The key matches one from predefined_keys
                # Create a new list with the value corresponding to the key
                new_list = [value[list(value.keys())[0]]]
                # Replace the original value with the new list
                data[key] = new_list
            # Check if value is a list with one item, and that item is a dict with exactly one key
            elif (
                isinstance(value, list)
                and len(value) == 1  # The list has exactly one element
                # The first item in the list is a dictionary
                and isinstance(value[0], dict)
                and len(value[0]) == 1  # The dictionary has exactly one key
                and list(value[0].keys())[0] in predefined_keys
            ):  # The key matches one from predefined_keys
                # Create a new list with the value corresponding to the key
                new_list = [value[0][list(value[0].keys())[0]]]
                # Replace the original value with the new list
                data[key] = new_list
            # Check if value is a list with one item, and that item is a dict with a key in special_keys list
            elif (
                isinstance(value, list)
                and len(value) == 1  # The list has exactly one element
                # The first item in the list is a dictionary
                and isinstance(value[0], dict)
                and list(value[0].keys())[0] in special_keys
            ):  # The key matches one from special_keys
                # Create a new list with the value corresponding to the key
                new_list = []
                new_list.extend(value[0][list(value[0].keys())[0]])
                # Replace the original value with the new list
                data[key] = new_list
            else:
                # If the value doesn't match the pattern, recursively call the function
                replace_specific_values(value, predefined_keys, special_keys)

    # Check if data is a list
    elif isinstance(data, list):
        # Iterate over each item in the list
        for item in data:
            # Recursively process each item in the list
            replace_specific_values(item, predefined_keys, special_keys)


def main():
    # Read JSON input from stdin
    input_data = sys.stdin.read()
    message_type = sys.argv[1]

    # -------------------------------------------------
    # For Xml
    data_dict = xmltodict.parse(input_data, force_list=["traces", "eventHistory"])
    # fix to remove top level element
    data_dict = data_dict[message_type]
    convert_dictionary(data_dict)
    # Can't handle recursion yet, which requires two passages
    replace_specific_values(data_dict, [], ["EventPoint"])
    replace_specific_values(data_dict, ["PathHistory"], [])
    replace_specific_values(data_dict, ["PathPoint"], [])

    # fix to set boolean values straigh
    # -------------------------------------------------
    DATA_FOLDER = os.path.join(os.path.dirname(__file__), "asn")
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

    # Uncomment only for debugging purposes. It won't work inside Nifi processing
    # print(data_dict)

    # Extract the 3 main elements from DenmEtsi (GeoNetwork and BTPB headers and inner DENM)
    data_dict_btpb = data_dict["btpb"]
    data_dict_denm = data_dict["denm"]
    data_dict_gn = data_dict["gbcGacHeader"]

    # Encode BTPB and DENM, to calculate the generated size
    encoded_btpb = encoder.encode("BTPB", data_dict_btpb)
    encoded_denm = encoder.encode("DENM", data_dict_denm)
    calculated_size = len(encoded_btpb) + len(encoded_denm)
    # Uncomment only for debugging purposes. It won't work inside Nifi processing
    # print("Size: " + str(calculated_size))
    # Upload GeoNetwork Payload length with appropriate size
    data_dict_gn["commonHeader"]["payloadLength"] = calculated_size

    encoded_gn = encoder.encode("GbcGacHeader", data_dict_gn)

    # To used anymore to encode full message. Encoding done individually
    # encoded = encoder.encode(service_type, data_dict)
    # Generate full encoded message by concatenating the individual components
    encoded = encoded_gn + encoded_btpb + encoded_denm
    # Uncomment only for debugging purposes. It won't work inside Nifi processing
    # print(encoded)
    message = hexlify(encoded).decode("ascii")
    print(message)


try:
    main()

    if __name__ == "__main__":
        sys.exit(0)
except asn1tools.codecs.EncodeError as e:
    sys.stderr.write(f"EncodeError: {e}\n")

    if __name__ == "__main__":
        sys.exit(1)
