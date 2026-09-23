def close(fig=None):
    """
    Close a figure window.

    Parameters
    ----------
    fig : None or int or str or `.Figure`
        The figure to close. There are a number of ways to specify this:

        - *None*: the current figure
        - `.Figure`: the given `.Figure` instance
        - ``int``: a figure number
        - ``str``: a figure name
        - 'all': all figures

    """
    if fig is None:
        manager = _pylab_helpers.Gcf.get_active()
        if manager is None:
            return
        else:
            _pylab_helpers.Gcf.destroy(manager)
    elif fig == 'all':
        _pylab_helpers.Gcf.destroy_all()
    elif isinstance(fig, int):
        _pylab_helpers.Gcf.destroy(fig)
    elif hasattr(fig, 'int'):
        # if we are dealing with a type UUID, we
        # can use its integer representation
        _pylab_helpers.Gcf.destroy(fig.int)
    elif isinstance(fig, str):
        all_labels = get_figlabels()
        if fig in all_labels:
            num = get_fignums()[all_labels.index(fig)]
            _pylab_helpers.Gcf.destroy(num)
    elif isinstance(fig, Figure):
        _pylab_helpers.Gcf.destroy_fig(fig)
    else:
        raise TypeError("close() argument must be a Figure, an int, a string, "
                        "or None, not %s" % type(fig))
