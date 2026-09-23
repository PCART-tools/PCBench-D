def ensure_int_or_float(arr: ArrayLike, copy: bool = False) -> np.ndarray:
    """
    Ensure that an dtype array of some integer dtype
    has an int64 dtype if possible.
    If it's not possible, potentially because of overflow,
    convert the array to float64 instead.

    Parameters
    ----------
    arr : array-like
          The array whose data type we want to enforce.
    copy: bool
          Whether to copy the original array or reuse
          it in place, if possible.

    Returns
    -------
    out_arr : The input array cast as int64 if
              possible without overflow.
              Otherwise the input array cast to float64.

    Notes
    -----
    If the array is explicitly of type uint64 the type
    will remain unchanged.
    """
    # TODO: GH27506 potential bug with ExtensionArrays
    try:
        # error: Unexpected keyword argument "casting" for "astype"
        return arr.astype("int64", copy=copy, casting="safe")  # type: ignore[call-arg]
    except TypeError:
        pass
    try:
        # error: Unexpected keyword argument "casting" for "astype"
        return arr.astype("uint64", copy=copy, casting="safe")  # type: ignore[call-arg]
    except TypeError:
        if is_extension_array_dtype(arr.dtype):
            return arr.to_numpy(dtype="float64", na_value=np.nan)
        return arr.astype("float64", copy=copy)
