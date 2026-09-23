def _dict_compat(d):
    """
    Helper function to convert datetimelike-keyed dicts to Timestamp-keyed dict

    Parameters
    ----------
    d: dict like object

    Returns
    -------
    dict

    """
    return dict((_maybe_box_datetimelike(key), value)
                for key, value in iteritems(d))
