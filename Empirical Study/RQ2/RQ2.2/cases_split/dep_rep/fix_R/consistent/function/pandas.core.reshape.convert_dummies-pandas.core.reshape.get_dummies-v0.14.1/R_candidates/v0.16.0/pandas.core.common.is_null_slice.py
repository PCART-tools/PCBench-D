def is_null_slice(obj):
    return (isinstance(obj, slice) and obj.start is None and
            obj.stop is None and obj.step is None)
