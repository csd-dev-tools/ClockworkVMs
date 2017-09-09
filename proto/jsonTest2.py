#!/usr/bin/python

import json

with open('configTwo.json') as json_data_file:
    data = json.load(json_data_file)
print(data)

print json.dumps(data, indent=4, sort_keys=True)

