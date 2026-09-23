def _resample_series(series, start, end, reindex_closed, rule,
                     resample_kwargs, how, fill_value):
    out = getattr(series.resample(rule, **resample_kwargs), how)()
    return out.reindex(pd.date_range(start, end, freq=rule,
                                     closed=reindex_closed),
                       fill_value=fill_value)
