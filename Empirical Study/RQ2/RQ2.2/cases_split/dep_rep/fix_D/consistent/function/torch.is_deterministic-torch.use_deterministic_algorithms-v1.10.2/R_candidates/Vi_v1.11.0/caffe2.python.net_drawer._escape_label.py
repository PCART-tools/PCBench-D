def _escape_label(name):
    # json.dumps is poor man's escaping
    return json.dumps(name)
