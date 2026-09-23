def _has_metadata(dt):
    if dt.metadata is not None:
        return True
    elif dt.names is not None:
        return any(_has_metadata(dt[k]) for k in dt.names)
    elif dt.subdtype is not None:
        return _has_metadata(dt.base)
    else:
        return False
