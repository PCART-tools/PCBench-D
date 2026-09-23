def fignum_exists(num):
    """Return whether the figure with the given id exists."""
    return _pylab_helpers.Gcf.has_fignum(num) or num in get_figlabels()
