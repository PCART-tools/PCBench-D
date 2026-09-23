def get_fignums():
    """Return a list of existing figure numbers."""
    return sorted(_pylab_helpers.Gcf.figs)
