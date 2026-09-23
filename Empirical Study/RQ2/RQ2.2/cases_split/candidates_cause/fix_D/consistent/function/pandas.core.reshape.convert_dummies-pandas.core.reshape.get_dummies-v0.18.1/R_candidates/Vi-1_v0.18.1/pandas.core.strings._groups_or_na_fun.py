def _groups_or_na_fun(regex):
    """Used in both extract_noexpand and extract_frame"""
    if regex.groups == 0:
        raise ValueError("pattern contains no capture groups")
    empty_row = [np.nan] * regex.groups

    def f(x):
        if not isinstance(x, compat.string_types):
            return empty_row
        m = regex.search(x)
        if m:
            return [np.nan if item is None else item for item in m.groups()]
        else:
            return empty_row
    return f
