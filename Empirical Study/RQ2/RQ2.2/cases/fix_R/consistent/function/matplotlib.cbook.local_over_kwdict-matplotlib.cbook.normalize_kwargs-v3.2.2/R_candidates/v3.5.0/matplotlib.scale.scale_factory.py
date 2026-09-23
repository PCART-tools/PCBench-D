def scale_factory(scale, axis, **kwargs):
    """
    Return a scale class by name.

    Parameters
    ----------
    scale : {%(names)s}
    axis : `matplotlib.axis.Axis`
    """
    if scale != scale.lower():
        _api.warn_deprecated(
            "3.5", message="Support for case-insensitive scales is deprecated "
            "since %(since)s and support will be removed %(removal)s.")
        scale = scale.lower()
    scale_cls = _api.check_getitem(_scale_mapping, scale=scale)
    return scale_cls(axis, **kwargs)
