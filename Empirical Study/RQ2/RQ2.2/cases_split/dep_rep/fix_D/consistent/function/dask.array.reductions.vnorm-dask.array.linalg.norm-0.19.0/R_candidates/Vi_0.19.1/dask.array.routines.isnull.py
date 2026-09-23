def isnull(values):
    """ pandas.isnull for dask arrays """
    # eagerly raise ImportError, if pandas isn't available
    import pandas as pd  # noqa
    return elemwise(_asarray_isnull, values, dtype='bool')
