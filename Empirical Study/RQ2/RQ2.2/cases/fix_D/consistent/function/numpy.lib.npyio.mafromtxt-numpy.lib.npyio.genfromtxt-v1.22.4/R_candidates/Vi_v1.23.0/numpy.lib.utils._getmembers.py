def _getmembers(item):
    import inspect
    try:
        members = inspect.getmembers(item)
    except Exception:
        members = [(x, getattr(item, x)) for x in dir(item)
                   if hasattr(item, x)]
    return members
