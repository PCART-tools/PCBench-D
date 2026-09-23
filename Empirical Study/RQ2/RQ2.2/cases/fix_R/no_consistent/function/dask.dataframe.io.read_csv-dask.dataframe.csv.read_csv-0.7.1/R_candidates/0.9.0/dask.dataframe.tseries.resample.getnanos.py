def getnanos(rule):
    try:
        return getattr(rule, 'nanos', None)
    except ValueError:
        return None
