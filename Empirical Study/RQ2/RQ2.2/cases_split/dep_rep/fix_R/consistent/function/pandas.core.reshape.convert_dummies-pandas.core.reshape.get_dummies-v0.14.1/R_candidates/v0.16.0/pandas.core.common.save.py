def save(obj, path):  # TODO remove in 0.13
    """
    Pickle (serialize) object to input file path

    Parameters
    ----------
    obj : any object
    path : string
        File path
    """
    import warnings
    warnings.warn("save is deprecated, use obj.to_pickle", FutureWarning)
    from pandas.io.pickle import to_pickle
    return to_pickle(obj, path)
