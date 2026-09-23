def check_lasso_selector(**kwargs):
    ax = get_ax()

    def onselect(verts):
        ax._got_onselect = True
        assert verts == [(100, 100), (125, 125), (150, 150)]

    tool = widgets.LassoSelector(ax, onselect, **kwargs)
    do_event(tool, 'press', xdata=100, ydata=100, button=1)
    do_event(tool, 'onmove', xdata=125, ydata=125, button=1)
    do_event(tool, 'release', xdata=150, ydata=150, button=1)

    assert ax._got_onselect
