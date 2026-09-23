def visualize(profilers, file_path=None, show=True, save=True, **kwargs):
    """Visualize the results of profiling in a bokeh plot.

    If multiple profilers are passed in, the plots are stacked vertically.

    Parameters
    ----------
    profilers : profiler or list
        Profiler or list of profilers.
    file_path : string, optional
        Name of the plot output file.
    show : boolean, optional
        If True (default), the plot is opened in a browser.
    save : boolean, optional
        If True (default), the plot is saved to disk.
    **kwargs
        Other keyword arguments, passed to bokeh.figure. These will override
        all defaults set by visualize.

    Returns
    -------
    The completed bokeh plot object.
    """
    bp = import_required('bokeh.plotting', _BOKEH_MISSING_MSG)
    from bokeh.io import _state

    if not _state._notebook:
        file_path = file_path or "profile.html"
        bp.output_file(file_path)

    if not isinstance(profilers, list):
        profilers = [profilers]
    figs = [prof._plot(**kwargs) for prof in profilers]
    # Stack the plots
    if len(figs) == 1:
        p = figs[0]
    else:
        top = figs[0]
        for f in figs[1:]:
            f.x_range = top.x_range
            f.title = None
            f.min_border_top = 20
            f.plot_height -= 30
        for f in figs[:-1]:
            f.xaxis.axis_label = None
            f.min_border_bottom = 20
            f.plot_height -= 30
        for f in figs:
            f.min_border_left = 75
            f.min_border_right = 75
        p = bp.gridplot([[f] for f in figs])
    if show:
        bp.show(p)
    if file_path and save:
        bp.save(p)
    return p
