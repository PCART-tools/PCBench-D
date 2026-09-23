def _resample_series(series, start, end, reindex_closed, rule,
                     resample_kwargs, how, fill_value):
    out = _resample_apply(series, rule, how, resample_kwargs)
    return out.reindex(pd.date_range(start, end, freq=rule,
                                     closed=reindex_closed),
                       fill_value=fill_value)
