@pytest.mark.parametrize(
    "x, y", [(42, 24), (None, 42), (None, None), (200, 100.01), (205.75, 2.0)])
def test_location_event_position(x, y):
    # LocationEvent should cast its x and y arguments to int unless it is None.
    fig, ax = plt.subplots()
    canvas = FigureCanvasBase(fig)
    event = LocationEvent("test_event", canvas, x, y)
    if x is None:
        assert event.x is None
    else:
        assert event.x == int(x)
        assert isinstance(event.x, int)
    if y is None:
        assert event.y is None
    else:
        assert event.y == int(y)
        assert isinstance(event.y, int)
    if x is not None and y is not None:
        assert re.match(
            "x={} +y={}".format(ax.format_xdata(x), ax.format_ydata(y)),
            ax.format_coord(x, y))
        ax.fmt_xdata = ax.fmt_ydata = lambda x: "foo"
        assert re.match("x=foo +y=foo", ax.format_coord(x, y))
