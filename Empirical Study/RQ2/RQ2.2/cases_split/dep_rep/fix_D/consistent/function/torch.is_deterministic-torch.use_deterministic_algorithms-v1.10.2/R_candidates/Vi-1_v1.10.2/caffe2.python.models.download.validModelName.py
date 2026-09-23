def validModelName(name):
    invalid_names = ['__init__']
    if name in invalid_names:
        return False
    if not re.match("^[/0-9a-zA-Z_-]+$", name):
        return False
    return True
