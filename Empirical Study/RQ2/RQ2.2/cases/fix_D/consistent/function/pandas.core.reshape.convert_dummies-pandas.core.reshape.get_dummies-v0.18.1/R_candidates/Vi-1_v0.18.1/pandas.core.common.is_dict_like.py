def is_dict_like(arg):
    return hasattr(arg, '__getitem__') and hasattr(arg, 'keys')
