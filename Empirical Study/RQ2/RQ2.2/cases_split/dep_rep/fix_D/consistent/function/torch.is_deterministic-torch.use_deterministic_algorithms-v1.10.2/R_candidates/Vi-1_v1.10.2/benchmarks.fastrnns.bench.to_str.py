def to_str(item):
    if isinstance(item, float):
        return '%.4g' % item
    return str(item)
