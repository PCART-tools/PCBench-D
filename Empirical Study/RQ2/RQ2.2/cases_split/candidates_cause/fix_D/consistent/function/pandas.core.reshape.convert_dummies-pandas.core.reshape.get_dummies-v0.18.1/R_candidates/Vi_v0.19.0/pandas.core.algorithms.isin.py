def isin(comps, values):
    """
    Compute the isin boolean array

    Parameters
    ----------
    comps: array-like
    values: array-like

    Returns
    -------
    boolean array same length as comps
    """

    if not is_list_like(comps):
        raise TypeError("only list-like objects are allowed to be passed"
                        " to isin(), you passed a "
                        "[{0}]".format(type(comps).__name__))
    comps = np.asarray(comps)
    if not is_list_like(values):
        raise TypeError("only list-like objects are allowed to be passed"
                        " to isin(), you passed a "
                        "[{0}]".format(type(values).__name__))
    if not isinstance(values, np.ndarray):
        values = list(values)

    # GH11232
    # work-around for numpy < 1.8 and comparisions on py3
    # faster for larger cases to use np.in1d
    if (_np_version_under1p8 and compat.PY3) or len(comps) > 1000000:
        f = lambda x, y: np.in1d(x, np.asarray(list(y)))
    else:
        f = lambda x, y: lib.ismember_int64(x, set(y))

    # may need i8 conversion for proper membership testing
    if is_datetime64_dtype(comps):
        from pandas.tseries.tools import to_datetime
        values = to_datetime(values)._values.view('i8')
        comps = comps.view('i8')
    elif is_timedelta64_dtype(comps):
        from pandas.tseries.timedeltas import to_timedelta
        values = to_timedelta(values)._values.view('i8')
        comps = comps.view('i8')
    elif is_int64_dtype(comps):
        pass
    else:
        f = lambda x, y: lib.ismember(x, set(values))

    return f(comps, values)
