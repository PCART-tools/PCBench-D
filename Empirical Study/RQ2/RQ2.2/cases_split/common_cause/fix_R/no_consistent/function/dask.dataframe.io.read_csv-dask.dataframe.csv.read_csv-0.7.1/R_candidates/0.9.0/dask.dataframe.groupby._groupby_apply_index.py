def _groupby_apply_index(df, ind, key, func):
    grouped = df.groupby(ind)
    grouped = _maybe_slice(grouped, key)
    return grouped.apply(func)
