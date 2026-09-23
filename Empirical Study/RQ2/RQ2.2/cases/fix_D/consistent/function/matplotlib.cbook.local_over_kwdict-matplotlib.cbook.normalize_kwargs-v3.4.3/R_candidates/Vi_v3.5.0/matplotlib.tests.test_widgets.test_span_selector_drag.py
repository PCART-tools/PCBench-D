@pytest.mark.parametrize('drag_from_anywhere', [True, False])
def test_span_selector_drag(drag_from_anywhere):
    ax = get_ax()

    def onselect(*args):
        pass

    # Create span
    tool = widgets.SpanSelector(ax, onselect, 'horizontal', interactive=True,
                                drag_from_anywhere=drag_from_anywhere)
    do_event(tool, 'press', xdata=10, ydata=10, button=1)
    do_event(tool, 'onmove', xdata=100, ydata=120, button=1)
    do_event(tool, 'release', xdata=100, ydata=120, button=1)
    assert tool.extents == (10, 100)
    # Drag inside span
    #
    # If drag_from_anywhere == True, this will move the span by 10,
    # giving new value extents = 20, 110
    #
    # If drag_from_anywhere == False, this will create a new span with
    # value extents = 25, 35
    do_event(tool, 'press', xdata=25, ydata=15, button=1)
    do_event(tool, 'onmove', xdata=35, ydata=25, button=1)
    do_event(tool, 'release', xdata=35, ydata=25, button=1)
    if drag_from_anywhere:
        assert tool.extents == (20, 110)
    else:
        assert tool.extents == (25, 35)

    # Check that in both cases, dragging outside the span draws a new span
    do_event(tool, 'press', xdata=175, ydata=185, button=1)
    do_event(tool, 'onmove', xdata=185, ydata=195, button=1)
    do_event(tool, 'release', xdata=185, ydata=195, button=1)
    assert tool.extents == (175, 185)
