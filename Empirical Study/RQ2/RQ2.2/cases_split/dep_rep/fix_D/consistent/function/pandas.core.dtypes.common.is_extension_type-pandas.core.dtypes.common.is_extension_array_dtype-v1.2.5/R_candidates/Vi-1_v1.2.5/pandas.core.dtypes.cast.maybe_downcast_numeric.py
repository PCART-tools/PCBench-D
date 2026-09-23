def maybe_downcast_numeric(result, dtype: DtypeObj, do_round: bool = False):
    """
    Subset of maybe_downcast_to_dtype restricted to numeric dtypes.

    Parameters
    ----------
    result : ndarray or ExtensionArray
    dtype : np.dtype or ExtensionDtype
    do_round : bool

    Returns
    -------
    ndarray or ExtensionArray
    """
    if not isinstance(dtype, np.dtype):
        # e.g. SparseDtype has no itemsize attr
        return result

    if isinstance(result, list):
        # reached via groupby.agg._ohlc; really this should be handled earlier
        result = np.array(result)

    def trans(x):
        if do_round:
            return x.round()
        return x

    if dtype.kind == result.dtype.kind:
        # don't allow upcasts here (except if empty)
        if result.dtype.itemsize <= dtype.itemsize and result.size:
            return result

    if is_bool_dtype(dtype) or is_integer_dtype(dtype):

        if not result.size:
            # if we don't have any elements, just astype it
            return trans(result).astype(dtype)

        # do a test on the first element, if it fails then we are done
        r = result.ravel()
        arr = np.array([r[0]])

        if isna(arr).any():
            # if we have any nulls, then we are done
            return result

        elif not isinstance(r[0], (np.integer, np.floating, int, float, bool)):
            # a comparable, e.g. a Decimal may slip in here
            return result

        if (
            issubclass(result.dtype.type, (np.object_, np.number))
            and notna(result).all()
        ):
            new_result = trans(result).astype(dtype)
            if new_result.dtype.kind == "O" or result.dtype.kind == "O":
                # np.allclose may raise TypeError on object-dtype
                if (new_result == result).all():
                    return new_result
            else:
                if np.allclose(new_result, result, rtol=0):
                    return new_result

    elif (
        issubclass(dtype.type, np.floating)
        and not is_bool_dtype(result.dtype)
        and not is_string_dtype(result.dtype)
    ):
        return result.astype(dtype)

    return result
