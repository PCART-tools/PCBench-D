def key_to_id(value):
    return [id(k) if key_is_id(k) else k for k in value.keys()]
