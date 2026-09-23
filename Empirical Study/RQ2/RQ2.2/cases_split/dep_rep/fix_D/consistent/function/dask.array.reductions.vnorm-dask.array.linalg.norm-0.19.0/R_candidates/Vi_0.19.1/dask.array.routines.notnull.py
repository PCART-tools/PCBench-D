def notnull(values):
    """ pandas.notnull for dask arrays """
    return ~isnull(values)
