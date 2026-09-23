def _checked_add_with_arr(arr, b):
    """
    Performs the addition of an int64 array and an int64 integer (or array)
    but checks that they do not result in overflow first.

    Parameters
    ----------
    arr : array addend.
    b : array or scalar addend.

    Returns
    -------
    sum : An array for elements x + b for each element x in arr if b is
          a scalar or an array for elements x + y for each element pair
          (x, y) in (arr, b).

    Raises
    ------
    OverflowError if any x + y exceeds the maximum int64 value.
    """
    if (np.iinfo(np.int64).max - b < arr).any():
        raise OverflowError("Python int too large to "
                            "convert to C long")
    return arr + b
