def test_rectangle_handles():
    ax = get_ax()

    def onselect(epress, erelease):
        pass

    tool = widgets.RectangleSelector(ax, onselect=onselect,
                                     grab_range=10,
                                     interactive=True,
                                     handle_props={'markerfacecolor': 'r',
                                                   'markeredgecolor': 'b'})
    tool.extents = (100, 150, 100, 150)

    assert tool.corners == (
        (100, 150, 150, 100), (100, 100, 150, 150))
    assert tool.extents == (100, 150, 100, 150)
    assert tool.edge_centers == (
        (100, 125.0, 150, 125.0), (125.0, 100, 125.0, 150))
    assert tool.extents == (100, 150, 100, 150)

    # grab a corner and move it
    do_event(tool, 'press', xdata=100, ydata=100)
    do_event(tool, 'onmove', xdata=120, ydata=120)
    do_event(tool, 'release', xdata=120, ydata=120)
    assert tool.extents == (120, 150, 120, 150)

    # grab the center and move it
    do_event(tool, 'press', xdata=132, ydata=132)
    do_event(tool, 'onmove', xdata=120, ydata=120)
    do_event(tool, 'release', xdata=120, ydata=120)
    assert tool.extents == (108, 138, 108, 138)

    # create a new rectangle
    do_event(tool, 'press', xdata=10, ydata=10)
    do_event(tool, 'onmove', xdata=100, ydata=100)
    do_event(tool, 'release', xdata=100, ydata=100)
    assert tool.extents == (10, 100, 10, 100)

    # Check that marker_props worked.
    assert mcolors.same_color(
        tool._corner_handles.artists[0].get_markerfacecolor(), 'r')
    assert mcolors.same_color(
        tool._corner_handles.artists[0].get_markeredgecolor(), 'b')
