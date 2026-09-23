def check_polygon_selector(event_sequence, expected_result, selections_count):
    """
    Helper function to test Polygon Selector.

    Parameters
    ----------
    event_sequence : list of tuples (etype, dict())
        A sequence of events to perform. The sequence is a list of tuples
        where the first element of the tuple is an etype (e.g., 'onmove',
        'press', etc.), and the second element of the tuple is a dictionary of
         the arguments for the event (e.g., xdata=5, key='shift', etc.).
    expected_result : list of vertices (xdata, ydata)
        The list of vertices that are expected to result from the event
        sequence.
    selections_count : int
        Wait for the tool to call its `onselect` function `selections_count`
        times, before comparing the result to the `expected_result`
    """
    ax = get_ax()

    ax._selections_count = 0

    def onselect(vertices):
        ax._selections_count += 1
        ax._current_result = vertices

    tool = widgets.PolygonSelector(ax, onselect)

    for (etype, event_args) in event_sequence:
        do_event(tool, etype, **event_args)

    assert ax._selections_count == selections_count
    assert ax._current_result == expected_result
