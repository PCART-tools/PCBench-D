def gcf():
    """
    Get the current figure.

    If no current figure exists, a new one is created using
    `~.pyplot.figure()`.
    """
    manager = _pylab_helpers.Gcf.get_active()
    if manager is not None:
        return manager.canvas.figure
    else:
        return figure()
