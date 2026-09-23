def ensure_categorical(arr):
    """
    Ensure that an array-like object is a Categorical (if not already).

    Parameters
    ----------
    arr : array-like
        The array that we want to convert into a Categorical.

    Returns
    -------
    cat_arr : The original array cast as a Categorical. If it already
              is a Categorical, we return as is.
    """

    if not is_categorical(arr):
        from pandas import Categorical

        arr = Categorical(arr)
    return arr
