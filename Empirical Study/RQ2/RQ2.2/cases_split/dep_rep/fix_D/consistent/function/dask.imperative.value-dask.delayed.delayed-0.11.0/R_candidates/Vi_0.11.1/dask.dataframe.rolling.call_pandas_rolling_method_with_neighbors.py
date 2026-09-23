def call_pandas_rolling_method_with_neighbors(prev_partition, this_partition,
                                              next_partition, before, after,
                                              rolling_kwargs, method_name,
                                              method_args, method_kwargs):

    if prev_partition.shape[0] != before or next_partition.shape[0] != after:
        raise NotImplementedError("Window requires larger inter-partition view than partition size")

    combined = pd.concat([prev_partition, this_partition, next_partition])
    method = getattr(combined.rolling(**rolling_kwargs), method_name)
    applied = method(*method_args, **method_kwargs)
    if after:
        return applied.iloc[before:-after]
    else:
        return applied.iloc[before:]
