def getfile(obj):
    try:
        return inspect.getfile(obj)
    except (TypeError, OSError):
        return None
