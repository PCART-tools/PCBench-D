def fillna_check(df, method, check=True):
    out = df.fillna(method=method)
    if check and out.isnull().values.all(axis=0).any():
        raise ValueError("All NaN partition encountered in `fillna`. Try "
                         "using ``df.repartition`` to increase the partition "
                         "size, or specify `limit` in `fillna`.")
    return out
