def _groupby_apply_level0(df, key, func):
    grouped = df.groupby(level=0)
    grouped = _maybe_slice(grouped, key)
    return grouped.apply(func)
