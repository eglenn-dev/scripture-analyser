import json
import os
import datetime as dt

def combine_json_files(directory):
    combined_data = {}
    combined_data['verses'] = []

    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]

    for json_file in json_files:
        with open(os.path.join(directory, json_file), 'r') as file:
            data = json.load(file)
            verses = data.get('verses', [])
            for verse in verses:
                combined_data['verses'].append(verse)

    combined_data['last-mod-date'] = str(dt.datetime.now())

    with open('data/combined.json', 'w') as file:
        json.dump(combined_data, file, indent=4)

combine_json_files('data/scriptures/flat')