def _cum_agg_filled(a, b, func, initial):
    union = a.index.union(b.index)
    return func(a.reindex(union, fill_value=initial),
                b.reindex(union, fill_value=initial), fill_value=initial)
