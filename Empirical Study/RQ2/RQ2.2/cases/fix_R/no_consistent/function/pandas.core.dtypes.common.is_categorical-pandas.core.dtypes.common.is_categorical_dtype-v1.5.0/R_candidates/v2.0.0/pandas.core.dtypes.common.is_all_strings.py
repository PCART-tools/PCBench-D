def is_all_strings(value: ArrayLike) -> bool:
    """
    Check if this is an array of strings that we should try parsing.

    Includes object-dtype ndarray containing all-strings, StringArray,
    and Categorical with all-string categories.
    Does not include numpy string dtypes.
    """
    dtype = value.dtype

    if isinstance(dtype, np.dtype):
        return (
            dtype == np.dtype("object")
            and lib.infer_dtype(value, skipna=False) == "string"
        )
    elif isinstance(dtype, CategoricalDtype):
        return dtype.categories.inferred_type == "string"
    return dtype == "string"
