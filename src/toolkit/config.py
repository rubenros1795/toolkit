import json 

def load(path):
    with open(path,'r') as f:
        config_json = json.load(f)
    return config_json