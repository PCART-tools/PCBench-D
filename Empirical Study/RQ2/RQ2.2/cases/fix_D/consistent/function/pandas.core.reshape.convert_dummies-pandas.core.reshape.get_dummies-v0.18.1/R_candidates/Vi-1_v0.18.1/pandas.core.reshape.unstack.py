def unstack(obj, level, fill_value=None):
    if isinstance(level, (tuple, list)):
        return _unstack_multiple(obj, level)

    if isinstance(obj, DataFrame):
        if isinstance(obj.index, MultiIndex):
            return _unstack_frame(obj, level, fill_value=fill_value)
        else:
            return obj.T.stack(dropna=False)
    else:
        unstacker = _Unstacker(obj.values, obj.index, level=level,
                               fill_value=fill_value)
        return unstacker.get_result()
