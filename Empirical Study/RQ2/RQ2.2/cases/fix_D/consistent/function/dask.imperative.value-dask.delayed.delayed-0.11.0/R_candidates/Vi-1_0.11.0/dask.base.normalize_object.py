@partial(normalize_token.register, object)
def normalize_object(o):
    if callable(o):
        return normalize_function(o)
    else:
        return uuid.uuid4().hex
