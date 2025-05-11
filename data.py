import json

_data = None

def load_data():
    global _data
    if not _data:
        with open("data.json", "r") as file:
            dataset = json.load(file)

            _data = {
                (record[0], record[1])
                for record in dataset
            }

def get_data():
    if not _data:
        load_data()
    return _data

print(get_data())