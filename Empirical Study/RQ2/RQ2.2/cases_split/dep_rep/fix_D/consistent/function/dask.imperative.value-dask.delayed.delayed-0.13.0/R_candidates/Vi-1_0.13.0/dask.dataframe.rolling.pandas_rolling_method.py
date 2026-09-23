def pandas_rolling_method(df, rolling_kwargs, name, *args, **kwargs):
    rolling = df.rolling(**rolling_kwargs)
    return getattr(rolling, name)(*args, **kwargs)
