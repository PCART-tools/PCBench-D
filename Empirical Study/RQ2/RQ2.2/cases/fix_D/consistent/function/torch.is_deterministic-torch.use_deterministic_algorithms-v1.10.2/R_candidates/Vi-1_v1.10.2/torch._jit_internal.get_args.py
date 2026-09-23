def get_args(target_type):
    return getattr(target_type, "__args__", None)
