@pytest.mark.parametrize('ignore_event_outside', [True, False])
def test_rectangle_selector_ignore_outside(ignore_event_outside):
    ax = get_ax()
    def onselect(vmin, vmax):
        ax._got_onselect = True

    tool = widgets.RectangleSelector(ax, onselect,
                                     ignore_event_outside=ignore_event_outside)
    do_event(tool, 'press', xdata=100, ydata=110, button=1)
    do_event(tool, 'onmove', xdata=150, ydata=120, button=1)
    do_event(tool, 'release', xdata=150, ydata=120, button=1)

    assert tool.ax._got_onselect
    assert tool.extents == (100.0, 150.0, 110.0, 120.0)

    # Reset
    ax._got_onselect = False
    # Trigger event outside of span
    do_event(tool, 'press', xdata=150, ydata=150, button=1)
    do_event(tool, 'onmove', xdata=160, ydata=160, button=1)
    do_event(tool, 'release', xdata=160, ydata=160, button=1)
    if ignore_event_outside:
        # event have been ignored and span haven't changed.
        assert not ax._got_onselect
        assert tool.extents == (100.0, 150.0, 110.0, 120.0)
    else:
        # A new shape is created
        assert ax._got_onselect
        assert tool.extents == (150.0, 160.0, 150.0, 160.0)
