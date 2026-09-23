def isna_all(arr: ArrayLike) -> bool:
    """
    Optimized equivalent to isna(arr).all()
    """
    total_len = len(arr)

    # Usually it's enough to check but a small fraction of values to see if
    #  a block is NOT null, chunks should help in such cases.
    #  parameters 1000 and 40 were chosen arbitrarily
    chunk_len = max(total_len // 40, 1000)

    dtype = arr.dtype
    if dtype.kind == "f":
        checker = nan_checker

    elif dtype.kind in ["m", "M"] or dtype.type is Period:
        checker = lambda x: np.asarray(x.view("i8")) == iNaT

    else:
        checker = lambda x: _isna_ndarraylike(x, inf_as_na=INF_AS_NA)

    for i in range(0, total_len, chunk_len):
        if not checker(arr[i : i + chunk_len]).all():
            return False

    return True
