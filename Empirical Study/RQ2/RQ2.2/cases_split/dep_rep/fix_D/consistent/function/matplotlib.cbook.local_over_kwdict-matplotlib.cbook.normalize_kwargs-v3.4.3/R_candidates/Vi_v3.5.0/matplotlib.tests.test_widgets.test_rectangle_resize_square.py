@pytest.mark.parametrize('use_default_state', [True, False])
def test_rectangle_resize_square(use_default_state):
    ax = get_ax()

    def onselect(epress, erelease):
        pass

    tool = widgets.RectangleSelector(ax, onselect, interactive=True)
    # Create rectangle
    _resize_rectangle(tool, 70, 65, 120, 115)
    assert tool.extents == (70.0, 120.0, 65.0, 115.0)

    if use_default_state:
        tool._default_state.add('square')
        use_key = None
    else:
        use_key = 'shift'

    # resize NE handle
    extents = tool.extents
    xdata, ydata = extents[1], extents[3]
    xdiff, ydiff = 10, 5
    xdata_new, ydata_new = xdata + xdiff, ydata + ydiff
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new, use_key)
    assert tool.extents == (extents[0], xdata_new,
                            extents[2], extents[3] + xdiff)

    # resize E handle
    extents = tool.extents
    xdata, ydata = extents[1], extents[2] + (extents[3] - extents[2]) / 2
    xdiff = 10
    xdata_new, ydata_new = xdata + xdiff, ydata
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new, use_key)
    assert tool.extents == (extents[0], xdata_new,
                            extents[2], extents[3] + xdiff)

    # resize E handle negative diff
    extents = tool.extents
    xdata, ydata = extents[1], extents[2] + (extents[3] - extents[2]) / 2
    xdiff = -20
    xdata_new, ydata_new = xdata + xdiff, ydata
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new, use_key)
    assert tool.extents == (extents[0], xdata_new,
                            extents[2], extents[3] + xdiff)

    # resize W handle
    extents = tool.extents
    xdata, ydata = extents[0], extents[2] + (extents[3] - extents[2]) / 2
    xdiff = 15
    xdata_new, ydata_new = xdata + xdiff, ydata
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new, use_key)
    assert tool.extents == (xdata_new, extents[1],
                            extents[2], extents[3] - xdiff)

    # resize W handle negative diff
    extents = tool.extents
    xdata, ydata = extents[0], extents[2] + (extents[3] - extents[2]) / 2
    xdiff = -25
    xdata_new, ydata_new = xdata + xdiff, ydata
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new, use_key)
    assert tool.extents == (xdata_new, extents[1],
                            extents[2], extents[3] - xdiff)

    # resize SW handle
    extents = tool.extents
    xdata, ydata = extents[0], extents[2]
    xdiff, ydiff = 20, 25
    xdata_new, ydata_new = xdata + xdiff, ydata + ydiff
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new, use_key)
    assert tool.extents == (extents[0] + ydiff, extents[1],
                            ydata_new, extents[3])
