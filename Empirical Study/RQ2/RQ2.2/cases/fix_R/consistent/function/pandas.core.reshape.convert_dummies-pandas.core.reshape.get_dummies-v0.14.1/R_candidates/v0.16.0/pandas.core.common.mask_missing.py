def mask_missing(arr, values_to_mask):
    """
    Return a masking array of same size/shape as arr
    with entries equaling any member of values_to_mask set to True
    """
    if not isinstance(values_to_mask, (list, np.ndarray)):
        values_to_mask = [values_to_mask]

    try:
        values_to_mask = np.array(values_to_mask, dtype=arr.dtype)
    except Exception:
        values_to_mask = np.array(values_to_mask, dtype=object)

    na_mask = isnull(values_to_mask)
    nonna = values_to_mask[~na_mask]

    mask = None
    for x in nonna:
        if mask is None:
            mask = arr == x

            # if x is a string and arr is not, then we get False and we must
            # expand the mask to size arr.shape
            if np.isscalar(mask):
                mask = np.zeros(arr.shape, dtype=bool)
        else:
            mask |= arr == x

    if na_mask.any():
        if mask is None:
            mask = isnull(arr)
        else:
            mask |= isnull(arr)

    return mask
