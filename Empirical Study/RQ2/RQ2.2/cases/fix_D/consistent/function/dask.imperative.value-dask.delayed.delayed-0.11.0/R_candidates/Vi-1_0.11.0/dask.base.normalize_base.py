@partial(normalize_token.register, Base)
def normalize_base(b):
    return type(b).__name__, b.key
