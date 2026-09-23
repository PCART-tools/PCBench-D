def plot_resources(results, palette='YlGnBu', **kwargs):
    """Plot resource usage in a bokeh plot.

    Parameters
    ----------
    results : sequence
        Output of ResourceProfiler.results
    palette : string, optional
        Name of the bokeh palette to use, must be key in bokeh.palettes.brewer.
    **kwargs
        Other keyword arguments, passed to bokeh.figure. These will override
        all defaults set by plot_resources.

    Returns
    -------
    The completed bokeh plot object.
    """
    bp = import_required('bokeh.plotting', _BOKEH_MISSING_MSG)
    from bokeh.palettes import brewer
    from bokeh.models import LinearAxis, Range1d

    defaults = dict(title="Profile Results",
                    tools="save,reset,resize,xwheel_zoom,xpan",
                    plot_width=800, plot_height=300)
    defaults.update((k, v) for (k, v) in kwargs.items() if k in
                    _get_figure_keywords())
    if results:
        t, mem, cpu = zip(*results)
        left, right = min(t), max(t)
        t = [i - left for i in t]
        p = bp.figure(y_range=(0, max(cpu)), x_range=(0, right - left), **defaults)
    else:
        t = mem = cpu = []
        p = bp.figure(y_range=(0, 100), x_range=(0, 10), **defaults)
    colors = brewer[palette][6]
    p.line(t, cpu, color=colors[0], line_width=4, legend='% CPU')
    p.yaxis.axis_label = "% CPU"
    p.extra_y_ranges = {'memory': Range1d(start=(min(mem) if mem else 0),
                                          end=(max(mem) if mem else 100))}
    p.line(t, mem, color=colors[2], y_range_name='memory', line_width=4,
           legend='Memory')
    p.add_layout(LinearAxis(y_range_name='memory', axis_label='Memory (MB)'),
                 'right')
    p.xaxis.axis_label = "Time (s)"
    return p
