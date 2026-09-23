def call_pandas_rolling_method_single(this_partition, rolling_kwargs,
                                      method_name, method_args, method_kwargs):
    # used for the start of the df/series (or for rolling through columns)
    method = getattr(this_partition.rolling(**rolling_kwargs), method_name)
    return method(*method_args, **method_kwargs)
