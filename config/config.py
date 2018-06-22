import json

with open('config/config.json', 'r') as tmp:
    conf = json.loads(tmp.read())
    token = conf['token']
    cogs_dir = 'cogs.'
    owner_id = conf['owner_id']
