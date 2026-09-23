@pytest.mark.parametrize(
    "data, text", [
        ([[10001, 10000]], "[10001.000]"),
        ([[.123, .987]], "[0.123]"),
        ([[np.nan, 1, 2]], "[]"),
        ([[1, 1+1e-15]], "[1.0000000000000000]"),
    ])
def test_format_cursor_data(data, text):
    from matplotlib.backend_bases import MouseEvent

    fig, ax = plt.subplots()
    im = ax.imshow(data)

    xdisp, ydisp = ax.transData.transform([0, 0])
    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.format_cursor_data(im.get_cursor_data(event)) == text
