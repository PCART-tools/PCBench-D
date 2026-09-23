def plot_tasks(results, dsk, palette='YlGnBu', label_size=60, **kwargs):
    """Visualize the results of profiling in a bokeh plot.

    Parameters
    ----------
    results : sequence
        Output of Profiler.results
    dsk : dict
        The dask graph being profiled.
    palette : string, optional
        Name of the bokeh palette to use, must be key in bokeh.palettes.brewer.
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
                    tools="hover,save,reset,resize,xwheel_zoom,xpan",
                    plot_width=800, plot_height=300)
    defaults.update((k, v) for (k, v) in kwargs.items() if k in
                    _get_figure_keywords())

    if results:
        keys, tasks, starts, ends, ids = zip(*results)

        id_group = tz.groupby(itemgetter(4), results)
        timings = dict((k, [i.end_time - i.start_time for i in v]) for (k, v) in
                    id_group.items())
        id_lk = dict((t[0], n) for (n, t) in enumerate(sorted(timings.items(),
                    key=itemgetter(1), reverse=True)))

        left = min(starts)
        right = max(ends)

        p = bp.figure(y_range=[str(i) for i in range(len(id_lk))],
                    x_range=[0, right - left], **defaults)

        data = {}
        data['width'] = width = [e - s for (s, e) in zip(starts, ends)]
        data['x'] = [w/2 + s - left for (w, s) in zip(width, starts)]
        data['y'] = [id_lk[i] + 1 for i in ids]
        data['function'] = funcs = [pprint_task(i, dsk, label_size) for i in tasks]
        data['color'] = get_colors(palette, funcs)
        data['key'] = [str(i) for i in keys]

        source = bp.ColumnDataSource(data=data)

        p.rect(source=source, x='x', y='y', height=1, width='width',
            color='color', line_color='gray')
    else:
        p = bp.figure(y_range=[str(i) for i in range(8)], x_range=[0, 10],
                      **defaults)
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.yaxis.axis_label = "Worker ID"
    p.xaxis.axis_label = "Time (s)"

    hover = p.select(HoverTool)
    hover.tooltips = """
    <div>
        <span style="font-size: 14px; font-weight: bold;">Key:</span>&nbsp;
        <span style="font-size: 10px; font-family: Monaco, monospace;">@key</span>
    </div>
    <div>
        <span style="font-size: 14px; font-weight: bold;">Task:</span>&nbsp;
        <span style="font-size: 10px; font-family: Monaco, monospace;">@function</span>
    </div>
    """
    hover.point_policy = 'follow_mouse'

    return p
