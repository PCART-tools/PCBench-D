def load(path):  # TODO remove in 0.13
    """
    Load pickled pandas object (or any other pickled object) from the specified
    file path

    Warning: Loading pickled data received from untrusted sources can be
    unsafe. See: http://docs.python.org/2.7/library/pickle.html

    Parameters
    ----------
    path : string
        File path

    Returns
    -------
    unpickled : type of object stored in file
    """
    import warnings
    warnings.warn("load is deprecated, use read_pickle", FutureWarning)
    from pandas.io.pickle import read_pickle
    return read_pickle(path)
