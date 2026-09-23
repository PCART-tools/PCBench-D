def np_pad(array, pad_width, mode, extra_arg=None):
    if mode in ["maximum", "mean", "median", "minimum"]:
        extra_arg = extra_arg or None
        return np.pad(array, pad_width, mode, stat_length=extra_arg)
    elif mode == "constant":
        extra_arg = extra_arg or 0
        return np.pad(array, pad_width, mode, constant_values=extra_arg)
    elif mode == "linear_ramp":
        extra_arg = extra_arg or 0
        return np.pad(array, pad_width, mode, end_values=extra_arg)
    elif mode in ["reflect", "symmetric"]:
        extra_arg = extra_arg or "even"
        return np.pad(array, pad_width, mode, reflect_type=extra_arg)
    else:
        return np.pad(array, pad_width, mode)
