def use_inf_as_null_cb(key):
    from pandas.types.missing import _use_inf_as_null
    _use_inf_as_null(key)
