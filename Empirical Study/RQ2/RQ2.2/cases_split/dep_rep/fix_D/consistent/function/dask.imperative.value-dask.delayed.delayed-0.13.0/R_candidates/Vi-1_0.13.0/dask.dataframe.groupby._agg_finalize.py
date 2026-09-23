def _agg_finalize(df, funcs):
    result = collections.OrderedDict()
    for result_column, func, kwargs in funcs:
        result[result_column] = func(df, **kwargs)

    return pd.DataFrame(result)
