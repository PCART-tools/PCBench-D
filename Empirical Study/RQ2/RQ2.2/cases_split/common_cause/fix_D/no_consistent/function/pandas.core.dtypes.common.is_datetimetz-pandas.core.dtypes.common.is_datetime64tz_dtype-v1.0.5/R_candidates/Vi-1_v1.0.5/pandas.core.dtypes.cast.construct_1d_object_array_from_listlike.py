def construct_1d_object_array_from_listlike(values):
    """
    Transform any list-like object in a 1-dimensional numpy array of object
    dtype.

    Parameters
    ----------
    values : any iterable which has a len()

    Raises
    ------
    TypeError
        * If `values` does not have a len()

    Returns
    -------
    1-dimensional numpy array of dtype object
    """
    # numpy will try to interpret nested lists as further dimensions, hence
    # making a 1D array that contains list-likes is a bit tricky:
    result = np.empty(len(values), dtype="object")
    result[:] = values
    return result
