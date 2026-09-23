@normalize_token.register((tuple, list))
def normalize_seq(seq):
    return type(seq).__name__, list(map(normalize_token, seq))
