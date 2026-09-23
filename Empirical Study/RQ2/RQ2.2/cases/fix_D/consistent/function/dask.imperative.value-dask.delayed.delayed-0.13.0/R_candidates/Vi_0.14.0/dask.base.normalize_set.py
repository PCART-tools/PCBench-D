@normalize_token.register(set)
def normalize_set(s):
    return normalize_token(sorted(s, key=str))
