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
from pathlib import Path
import json
import xmltodict
import xml.etree.ElementTree as ET
from binascii import hexlify

# Debug: Log the input data
# sys.stderr.write(f"Input data: {input_data}\n")

def convert_dictionary(data):
  if isinstance(data, dict):
    for key, value in data.items():
      #print("Processing key: ", key)
      if value in ['True', 'true']:
        data[key] = True
      elif isinstance(value, dict) and 'true' in value and value['true'] is None:
        data[key] = True
      elif value in ['False', 'false']:
        data[key] = False
      elif isinstance(value, dict) and 'false' in value and value['false'] is None:
        data[key] = False
      elif isinstance(value, dict) and len(value) == 1 and list(value.values())[0] is None:
        data[key] = list(value.keys())[0]        
      elif isinstance(value, str) and (value.isdigit() or (value.startswith('-') and value[1:].isdigit())):
        data[key] = int(value)
      elif isinstance(value, list) and value == [None]:
        data[key] = []
      else:
        convert_dictionary(value)
  elif isinstance(data, list):
    for item in data:
      convert_dictionary(item)

def replace_specific_values(data, predefined_keys):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) and len(value) == 1 and list(value.keys())[0] in predefined_keys:
                new_list = []
                new_list.append(value[list(value.keys())[0]])
                #print("Replacing key: ", key, " with value: ", new_list)
                data[key] = new_list
            elif isinstance(value, list) and len(value) == 1 and isinstance(value[0], dict) and len(value[0]) == 1 and list(value[0].keys())[0] in predefined_keys:
                new_list = []
                new_list.append(value[0][list(value[0].keys())[0]])
                #print("Replacing key: ", key, " with value: ", new_list)
                data[key] = new_list
            else:
                replace_specific_values(value, predefined_keys)
    elif isinstance(data, list):
        for item in data:
            replace_specific_values(item, predefined_keys)

try:  
  
  # Read JSON input from stdin
  input_data = sys.stdin.read()

  # messageType = os.environ.get("messageType")
  messageType = sys.argv[1]
  # print(f"messageType {messageType}")
  # -------------------------------------------------
  # For Json
  #data_dict = json.loads(input_data)
  # -------------------------------------------------
  # For Xml
  data_dict = xmltodict.parse(input_data, force_list=['traces', 'eventHistory'])
  # fix to remove top level element
  data_dict = data_dict['DenmEtsi']
  convert_dictionary(data_dict)
  # Can't handle recursion yet, which requires two passages
  replace_specific_values(data_dict,["EventPoint","PathHistory"])
  replace_specific_values(data_dict,["PathPoint"])

  # fix to set boolean values straigh         
  # -------------------------------------------------
# sys.stderr.write(f"Input data type: {type(data_dict)}\n")
  DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'asn')
  asn1_files = [os.path.join(DATA_FOLDER, f) for f in os.listdir(DATA_FOLDER) if f.endswith('.asn')]
  encoder = asn1tools.compile_files(asn1_files, codec='uper', any_defined_by_choices=None, encoding='utf-8', numeric_enums=False)
  service_type = messageType

# # Encode the data
# try:
  encoded = encoder.encode(service_type, data_dict)
    # Debug: Log the encoded data
    # sys.stderr.write(f"Encoded data: {encoded}\n")
  message = hexlify(encoded).decode('ascii')
  print(message)
  sys.exit(0)
except asn1tools.codecs.EncodeError as e:
    sys.stderr.write(f"EncodeError: {e}\n")
    sys.exit(1)