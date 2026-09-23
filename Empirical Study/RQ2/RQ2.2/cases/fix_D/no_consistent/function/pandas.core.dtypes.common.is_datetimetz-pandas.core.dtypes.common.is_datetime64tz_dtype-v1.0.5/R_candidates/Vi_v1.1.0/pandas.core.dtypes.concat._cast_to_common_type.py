def _cast_to_common_type(arr: ArrayLike, dtype: DtypeObj) -> ArrayLike:
    """
    Helper function for `arr.astype(common_dtype)` but handling all special
    cases.
    """
    if (
        is_categorical_dtype(arr.dtype)
        and isinstance(dtype, np.dtype)
        and np.issubdtype(dtype, np.integer)
    ):
        # problem case: categorical of int -> gives int as result dtype,
        # but categorical can contain NAs -> fall back to object dtype
        try:
            return arr.astype(dtype, copy=False)
        except ValueError:
            return arr.astype(object, copy=False)

    if is_sparse(arr) and not is_sparse(dtype):
        # problem case: SparseArray.astype(dtype) doesn't follow the specified
        # dtype exactly, but converts this to Sparse[dtype] -> first manually
        # convert to dense array
        arr = cast(SparseArray, arr)
        return arr.to_dense().astype(dtype, copy=False)

    if (
        isinstance(arr, np.ndarray)
        and arr.dtype.kind in ["m", "M"]
        and dtype is np.dtype("object")
    ):
        # wrap datetime-likes in EA to ensure astype(object) gives Timestamp/Timedelta
        # this can happen when concat_compat is called directly on arrays (when arrays
        # are not coming from Index/Series._values), eg in BlockManager.quantile
        arr = array(arr)

    if is_extension_array_dtype(dtype):
        if isinstance(arr, np.ndarray):
            # numpy's astype cannot handle ExtensionDtypes
            return array(arr, dtype=dtype, copy=False)
    return arr.astype(dtype, copy=False)
