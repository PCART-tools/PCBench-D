def get_origin(target_type):
    return getattr(target_type, "__origin__", None)
