def check_span(*args, **kwargs):
    ax = get_ax()

    def onselect(vmin, vmax):
        ax._got_onselect = True
        assert vmin == 100
        assert vmax == 150

    def onmove(vmin, vmax):
        assert vmin == 100
        assert vmax == 125
        ax._got_on_move = True

    if 'onmove_callback' in kwargs:
        kwargs['onmove_callback'] = onmove

    tool = widgets.SpanSelector(ax, onselect, *args, **kwargs)
    do_event(tool, 'press', xdata=100, ydata=100, button=1)
    do_event(tool, 'onmove', xdata=125, ydata=125, button=1)
    do_event(tool, 'release', xdata=150, ydata=150, button=1)

    assert ax._got_onselect

    if 'onmove_callback' in kwargs:
        assert ax._got_on_move
