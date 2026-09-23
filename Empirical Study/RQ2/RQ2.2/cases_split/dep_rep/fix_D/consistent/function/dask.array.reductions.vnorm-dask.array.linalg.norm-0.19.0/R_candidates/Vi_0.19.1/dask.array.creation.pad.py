@wraps(np.pad)
def pad(array, pad_width, mode, **kwargs):
    array = asarray(array)

    pad_width = expand_pad_width(array, pad_width)

    if mode in ["maximum", "mean", "median", "minimum"]:
        kwargs.setdefault("stat_length", array.shape)
    elif mode == "constant":
        kwargs.setdefault("constant_values", 0)
    elif mode == "linear_ramp":
        kwargs.setdefault("end_values", 0)
    elif mode in ["reflect", "symmetric"]:
        kwargs.setdefault("reflect_type", "even")
    elif mode in ["edge", "wrap"]:
        if kwargs:
            raise TypeError("Got unsupported keyword arguments.")
    elif callable(mode):
        kwargs.setdefault("kwargs", {})
    else:
        raise ValueError("Got an unsupported `mode`.")

    if not callable(mode) and len(kwargs) > 1:
        raise TypeError("Got too many keyword arguments.")

    if mode in ["maximum", "mean", "median", "minimum"]:
        return pad_stats(array, pad_width, mode, *kwargs.values())
    elif mode in ["constant", "edge", "linear_ramp"]:
        return pad_edge(array, pad_width, mode, *kwargs.values())
    elif mode in ["reflect", "symmetric", "wrap"]:
        return pad_reuse(array, pad_width, mode, *kwargs.values())
    elif callable(mode):
        return pad_udf(array, pad_width, mode, **kwargs)
    else:
        raise ValueError("Unsupported mode selected.")
