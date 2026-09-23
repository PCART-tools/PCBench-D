def test_ellipse():
    """For ellipse, test out the key modifiers"""
    ax = get_ax()

    def onselect(epress, erelease):
        pass

    tool = widgets.EllipseSelector(ax, onselect=onselect,
                                   maxdist=10, interactive=True)
    tool.extents = (100, 150, 100, 150)

    # drag the rectangle
    do_event(tool, 'press', xdata=10, ydata=10, button=1,
             key=' ')

    do_event(tool, 'onmove', xdata=30, ydata=30, button=1)
    do_event(tool, 'release', xdata=30, ydata=30, button=1)
    assert tool.extents == (120, 170, 120, 170)

    # create from center
    do_event(tool, 'on_key_press', xdata=100, ydata=100, button=1,
             key='control')
    do_event(tool, 'press', xdata=100, ydata=100, button=1)
    do_event(tool, 'onmove', xdata=125, ydata=125, button=1)
    do_event(tool, 'release', xdata=125, ydata=125, button=1)
    do_event(tool, 'on_key_release', xdata=100, ydata=100, button=1,
             key='control')
    assert tool.extents == (75, 125, 75, 125)

    # create a square
    do_event(tool, 'on_key_press', xdata=10, ydata=10, button=1,
             key='shift')
    do_event(tool, 'press', xdata=10, ydata=10, button=1)
    do_event(tool, 'onmove', xdata=35, ydata=30, button=1)
    do_event(tool, 'release', xdata=35, ydata=30, button=1)
    do_event(tool, 'on_key_release', xdata=10, ydata=10, button=1,
             key='shift')
    extents = [int(e) for e in tool.extents]
    assert extents == [10, 35, 10, 34]

    # create a square from center
    do_event(tool, 'on_key_press', xdata=100, ydata=100, button=1,
             key='ctrl+shift')
    do_event(tool, 'press', xdata=100, ydata=100, button=1)
    do_event(tool, 'onmove', xdata=125, ydata=130, button=1)
    do_event(tool, 'release', xdata=125, ydata=130, button=1)
    do_event(tool, 'on_key_release', xdata=100, ydata=100, button=1,
             key='ctrl+shift')
    extents = [int(e) for e in tool.extents]
    assert extents == [70, 129, 70, 130]

    assert tool.geometry.shape == (2, 73)
    assert_allclose(tool.geometry[:, 0], [70., 100])
