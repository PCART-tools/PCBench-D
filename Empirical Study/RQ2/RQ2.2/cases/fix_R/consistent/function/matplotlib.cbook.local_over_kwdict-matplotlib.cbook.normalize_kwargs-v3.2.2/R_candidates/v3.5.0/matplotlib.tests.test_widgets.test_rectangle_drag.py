@pytest.mark.parametrize('drag_from_anywhere, new_center',
                         [[True, (60, 75)],
                          [False, (30, 20)]])
def test_rectangle_drag(drag_from_anywhere, new_center):
    ax = get_ax()

    def onselect(epress, erelease):
        pass

    tool = widgets.RectangleSelector(ax, onselect, interactive=True,
                                     drag_from_anywhere=drag_from_anywhere)
    # Create rectangle
    do_event(tool, 'press', xdata=0, ydata=10, button=1)
    do_event(tool, 'onmove', xdata=100, ydata=120, button=1)
    do_event(tool, 'release', xdata=100, ydata=120, button=1)
    assert tool.center == (50, 65)
    # Drag inside rectangle, but away from centre handle
    #
    # If drag_from_anywhere == True, this will move the rectangle by (10, 10),
    # giving it a new center of (60, 75)
    #
    # If drag_from_anywhere == False, this will create a new rectangle with
    # center (30, 20)
    do_event(tool, 'press', xdata=25, ydata=15, button=1)
    do_event(tool, 'onmove', xdata=35, ydata=25, button=1)
    do_event(tool, 'release', xdata=35, ydata=25, button=1)
    assert tool.center == new_center
    # Check that in both cases, dragging outside the rectangle draws a new
    # rectangle
    do_event(tool, 'press', xdata=175, ydata=185, button=1)
    do_event(tool, 'onmove', xdata=185, ydata=195, button=1)
    do_event(tool, 'release', xdata=185, ydata=195, button=1)
    assert tool.center == (180, 190)
