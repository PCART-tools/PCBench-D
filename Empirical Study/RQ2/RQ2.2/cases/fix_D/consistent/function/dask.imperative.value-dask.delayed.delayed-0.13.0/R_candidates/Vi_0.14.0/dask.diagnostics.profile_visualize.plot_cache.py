def plot_cache(results, dsk, start_time, metric_name, palette='Viridis',
               label_size=60, **kwargs):
    """Visualize the results of profiling in a bokeh plot.

    Parameters
    ----------
    results : sequence
        Output of CacheProfiler.results
    dsk : dict
        The dask graph being profiled.
    start_time : float
        Start time of the profile.
    metric_name : string
        Metric used to measure cache size
    palette : string, optional
        Name of the bokeh palette to use, must be a member of
        bokeh.palettes.all_palettes.
    label_size: int (optional)
        Maximum size of output labels in plot, defaults to 60
    **kwargs
        Other keyword arguments, passed to bokeh.figure. These will override
        all defaults set by visualize.

    Returns
    -------
    The completed bokeh plot object.
    """
    bp = import_required('bokeh.plotting', _BOKEH_MISSING_MSG)
    from bokeh.models import HoverTool
    tz = import_required('toolz', _TOOLZ_MISSING_MSG)

    defaults = dict(title="Profile Results",
                    tools="hover,save,reset,resize,wheel_zoom,xpan",
                    plot_width=800, plot_height=300)
    defaults.update((k, v) for (k, v) in kwargs.items() if k in
                    _get_figure_keywords())

    if results:
        starts, ends = list(zip(*results))[3:]
        tics = list(sorted(tz.unique(starts + ends)))
        groups = tz.groupby(lambda d: pprint_task(d[1], dsk, label_size), results)
        data = {}
        for k, vals in groups.items():
            cnts = dict.fromkeys(tics, 0)
            for v in vals:
                cnts[v.cache_time] += v.metric
                cnts[v.free_time] -= v.metric
            data[k] = [0] + list(tz.accumulate(add, tz.pluck(1, sorted(cnts.items()))))

        tics = [0] + [i - start_time for i in tics]
        p = bp.figure(x_range=[0, max(tics)], **defaults)

        for (key, val), color in zip(data.items(), get_colors(palette, data.keys())):
            p.line('x', 'y', line_color=color, line_width=3,
                   source=bp.ColumnDataSource({'x': tics, 'y': val,
                                               'label': [key for i in val]}))

    else:
        p = bp.figure(y_range=[0, 10], x_range=[0, 10], **defaults)
    p.yaxis.axis_label = "Cache Size ({0})".format(metric_name)
    p.xaxis.axis_label = "Time (s)"

    hover = p.select(HoverTool)
    hover.tooltips = """
    <div>
        <span style="font-size: 14px; font-weight: bold;">Task:</span>&nbsp;
        <span style="font-size: 10px; font-family: Monaco, monospace;">@label</span>
    </div>
    """
    return p
