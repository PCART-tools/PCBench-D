@pytest.mark.parametrize('ignore_event_outside', [True, False])
def test_span_selector_ignore_outside(ignore_event_outside):
    ax = get_ax()
    def onselect(vmin, vmax):
        ax._got_onselect = True

    def onmove(vmin, vmax):
        ax._got_on_move = True

    tool = widgets.SpanSelector(ax, onselect, 'horizontal',
                                onmove_callback=onmove,
                                ignore_event_outside=ignore_event_outside)
    do_event(tool, 'press', xdata=100, ydata=100, button=1)
    do_event(tool, 'onmove', xdata=125, ydata=125, button=1)
    do_event(tool, 'release', xdata=125, ydata=125, button=1)
    assert ax._got_onselect
    assert ax._got_on_move
    assert tool.extents == (100, 125)

    # Reset
    ax._got_onselect = False
    ax._got_on_move = False
    # Trigger event outside of span
    do_event(tool, 'press', xdata=150, ydata=150, button=1)
    do_event(tool, 'onmove', xdata=160, ydata=160, button=1)
    do_event(tool, 'release', xdata=160, ydata=160, button=1)
    if ignore_event_outside:
        # event have been ignored and span haven't changed.
        assert not ax._got_onselect
        assert not ax._got_on_move
        assert tool.extents == (100, 125)
    else:
        # A new shape is created
        assert ax._got_onselect
        assert ax._got_on_move
        assert tool.extents == (150, 160)
