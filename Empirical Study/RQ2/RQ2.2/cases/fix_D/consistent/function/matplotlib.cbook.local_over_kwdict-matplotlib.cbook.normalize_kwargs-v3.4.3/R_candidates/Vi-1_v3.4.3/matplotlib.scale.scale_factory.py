def scale_factory(scale, axis, **kwargs):
    """
    Return a scale class by name.

    Parameters
    ----------
    scale : {%(names)s}
    axis : `matplotlib.axis.Axis`
    """
    scale = scale.lower()
    _api.check_in_list(_scale_mapping, scale=scale)
    return _scale_mapping[scale](axis, **kwargs)
