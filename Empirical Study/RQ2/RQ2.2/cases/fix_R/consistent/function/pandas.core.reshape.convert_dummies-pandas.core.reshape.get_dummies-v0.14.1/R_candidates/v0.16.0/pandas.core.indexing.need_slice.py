def need_slice(obj):
    return (obj.start is not None or
            obj.stop is not None or
            (obj.step is not None and obj.step != 1))
