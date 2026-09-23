@normalize_token.register(dict)
def normalize_dict(d):
    return normalize_token(sorted(d.items(), key=str))
