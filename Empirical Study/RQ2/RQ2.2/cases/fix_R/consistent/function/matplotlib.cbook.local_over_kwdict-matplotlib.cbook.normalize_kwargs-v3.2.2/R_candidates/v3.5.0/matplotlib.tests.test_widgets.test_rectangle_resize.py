def test_rectangle_resize():
    ax = get_ax()

    def onselect(epress, erelease):
        pass

    tool = widgets.RectangleSelector(ax, onselect, interactive=True)
    # Create rectangle
    _resize_rectangle(tool, 0, 10, 100, 120)
    assert tool.extents == (0.0, 100.0, 10.0, 120.0)

    # resize NE handle
    extents = tool.extents
    xdata, ydata = extents[1], extents[3]
    xdata_new, ydata_new = xdata + 10, ydata + 5
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new)
    assert tool.extents == (extents[0], xdata_new, extents[2], ydata_new)

    # resize E handle
    extents = tool.extents
    xdata, ydata = extents[1], extents[2] + (extents[3] - extents[2]) / 2
    xdata_new, ydata_new = xdata + 10, ydata
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new)
    assert tool.extents == (extents[0], xdata_new, extents[2], extents[3])

    # resize W handle
    extents = tool.extents
    xdata, ydata = extents[0], extents[2] + (extents[3] - extents[2]) / 2
    xdata_new, ydata_new = xdata + 15, ydata
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new)
    assert tool.extents == (xdata_new, extents[1], extents[2], extents[3])

    # resize SW handle
    extents = tool.extents
    xdata, ydata = extents[0], extents[2]
    xdata_new, ydata_new = xdata + 20, ydata + 25
    _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new)
    assert tool.extents == (xdata_new, extents[1], ydata_new, extents[3])
