def resample(df, freq, how='mean', **kwargs):
    return getattr(df.resample(freq, **kwargs), how)()
