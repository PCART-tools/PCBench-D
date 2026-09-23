def str_slice(arr, start=None, stop=None, step=None):
    """
    Slice substrings from each element in the Series/Index

    Parameters
    ----------
    start : int or None
    stop : int or None
    step : int or None

    Returns
    -------
    sliced : Series/Index of objects
    """
    obj = slice(start, stop, step)
    f = lambda x: x[obj]
    return _na_map(f, arr)
