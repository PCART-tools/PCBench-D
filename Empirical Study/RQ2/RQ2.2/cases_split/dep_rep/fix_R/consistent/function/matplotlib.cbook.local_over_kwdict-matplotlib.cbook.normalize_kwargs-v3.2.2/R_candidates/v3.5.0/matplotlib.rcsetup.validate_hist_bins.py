def validate_hist_bins(s):
    valid_strs = ["auto", "sturges", "fd", "doane", "scott", "rice", "sqrt"]
    if isinstance(s, str) and s in valid_strs:
        return s
    try:
        return int(s)
    except (TypeError, ValueError):
        pass
    try:
        return validate_floatlist(s)
    except ValueError:
        pass
    raise ValueError("'hist.bins' must be one of {}, an int or"
                     " a sequence of floats".format(valid_strs))
