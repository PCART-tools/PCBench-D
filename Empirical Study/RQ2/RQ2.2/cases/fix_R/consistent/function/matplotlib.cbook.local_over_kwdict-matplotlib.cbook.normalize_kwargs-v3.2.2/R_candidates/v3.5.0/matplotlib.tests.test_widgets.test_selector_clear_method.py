@pytest.mark.parametrize('selector', ['span', 'rectangle'])
def test_selector_clear_method(selector):
    ax = get_ax()

    def onselect(*args):
        pass

    if selector == 'span':
        tool = widgets.SpanSelector(ax, onselect, 'horizontal',
                                    interactive=True,
                                    ignore_event_outside=True)
    else:
        tool = widgets.RectangleSelector(ax, onselect, interactive=True)
    do_event(tool, 'press', xdata=10, ydata=10, button=1)
    do_event(tool, 'onmove', xdata=100, ydata=120, button=1)
    do_event(tool, 'release', xdata=100, ydata=120, button=1)
    assert tool._selection_completed
    assert tool.visible
    if selector == 'span':
        assert tool.extents == (10, 100)

    tool.clear()
    assert not tool._selection_completed
    assert not tool.visible

    # Do another cycle of events to make sure we can
    do_event(tool, 'press', xdata=10, ydata=10, button=1)
    do_event(tool, 'onmove', xdata=50, ydata=120, button=1)
    do_event(tool, 'release', xdata=50, ydata=120, button=1)
    assert tool._selection_completed
    assert tool.visible
    if selector == 'span':
        assert tool.extents == (10, 50)
