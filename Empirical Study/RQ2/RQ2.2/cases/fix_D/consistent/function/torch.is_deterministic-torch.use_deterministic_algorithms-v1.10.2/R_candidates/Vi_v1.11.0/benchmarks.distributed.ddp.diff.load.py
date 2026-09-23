def load(path):
    with open(path, 'r') as f:
        return json.load(f)
