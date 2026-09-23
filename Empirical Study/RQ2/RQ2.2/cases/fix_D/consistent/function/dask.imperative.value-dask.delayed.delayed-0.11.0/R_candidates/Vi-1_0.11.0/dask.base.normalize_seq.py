@partial(normalize_token.register, (tuple, list, set))
def normalize_seq(seq):
    return type(seq).__name__, list(map(normalize_token, seq))
