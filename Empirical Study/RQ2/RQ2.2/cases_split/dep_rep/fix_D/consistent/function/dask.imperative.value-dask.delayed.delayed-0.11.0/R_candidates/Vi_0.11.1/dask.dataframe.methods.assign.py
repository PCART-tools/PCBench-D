def assign(df, *pairs):
    kwargs = dict(partition(2, pairs))
    return df.assign(**kwargs)
