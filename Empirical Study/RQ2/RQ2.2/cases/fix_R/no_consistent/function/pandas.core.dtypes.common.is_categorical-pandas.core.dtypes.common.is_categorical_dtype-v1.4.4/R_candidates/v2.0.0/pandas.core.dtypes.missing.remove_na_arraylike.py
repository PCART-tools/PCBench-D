def remove_na_arraylike(arr):
    """
    Return array-like containing only true/non-NaN values, possibly empty.
    """
    if is_extension_array_dtype(arr):
        return arr[notna(arr)]
    else:
        return arr[notna(np.asarray(arr))]
