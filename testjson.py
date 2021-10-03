import json

with open('testprefs.json') as config_file:
    data = json.load(config_file)

width = data['firstName']
height = data['hobbies']
print(width)
print(height)