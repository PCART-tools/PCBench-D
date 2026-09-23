@pytest.mark.parametrize(
    "data, text_without_colorbar, text_with_colorbar", [
        ([[10001, 10000]], "[1e+04]", "[10001]"),
        ([[.123, .987]], "[0.123]", "[0.123]"),
])
def test_format_cursor_data(data, text_without_colorbar, text_with_colorbar):
    from matplotlib.backend_bases import MouseEvent

    fig, ax = plt.subplots()
    im = ax.imshow(data)

    xdisp, ydisp = ax.transData.transform([0, 0])
    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.get_cursor_data(event) == data[0][0]
    assert im.format_cursor_data(im.get_cursor_data(event)) \
        == text_without_colorbar

    fig.colorbar(im)
    fig.canvas.draw()  # This is necessary to set up the colorbar formatter.

    assert im.get_cursor_data(event) == data[0][0]
    assert im.format_cursor_data(im.get_cursor_data(event)) \
        == text_with_colorbar
