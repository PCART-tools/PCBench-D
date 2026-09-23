def fill_zeros(result, x, y, name, fill):
    """
    if this is a reversed op, then flip x,y

    if we have an integer value (or array in y)
    and we have 0's, fill them with the fill,
    return the result

    mask the nan's from x
    """
    if fill is None or is_float_dtype(result):
        return result

    if name.startswith(('r', '__r')):
        x, y = y, x

    is_variable_type = (hasattr(y, 'dtype') or hasattr(y, 'type'))
    is_scalar_type = is_scalar(y)

    if not is_variable_type and not is_scalar_type:
        return result

    if is_scalar_type:
        y = np.array(y)

    if is_integer_dtype(y):

        if (y == 0).any():

            # GH 7325, mask and nans must be broadcastable (also: PR 9308)
            # Raveling and then reshaping makes np.putmask faster
            mask = ((y == 0) & ~np.isnan(result)).ravel()

            shape = result.shape
            result = result.astype('float64', copy=False).ravel()

            np.putmask(result, mask, fill)

            # if we have a fill of inf, then sign it correctly
            # (GH 6178 and PR 9308)
            if np.isinf(fill):
                signs = np.sign(y if name.startswith(('r', '__r')) else x)
                negative_inf_mask = (signs.ravel() < 0) & mask
                np.putmask(result, negative_inf_mask, -fill)

            if "floordiv" in name:  # (PR 9308)
                nan_mask = ((y == 0) & (x == 0)).ravel()
                np.putmask(result, nan_mask, np.nan)

            result = result.reshape(shape)

    return result
