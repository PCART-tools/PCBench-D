def test_polygon_selector():
    # Simple polygon
    expected_result = [(50, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50))
    check_polygon_selector(event_sequence, expected_result, 1)

    # Move first vertex before completing the polygon.
    expected_result = [(75, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + [('on_key_press', dict(key='control')),
                         ('onmove', dict(xdata=50, ydata=50)),
                         ('press', dict(xdata=50, ydata=50)),
                         ('onmove', dict(xdata=75, ydata=50)),
                         ('release', dict(xdata=75, ydata=50)),
                         ('on_key_release', dict(key='control'))]
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(75, 50))
    check_polygon_selector(event_sequence, expected_result, 1)

    # Move first two vertices at once before completing the polygon.
    expected_result = [(50, 75), (150, 75), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + [('on_key_press', dict(key='shift')),
                         ('onmove', dict(xdata=100, ydata=100)),
                         ('press', dict(xdata=100, ydata=100)),
                         ('onmove', dict(xdata=100, ydata=125)),
                         ('release', dict(xdata=100, ydata=125)),
                         ('on_key_release', dict(key='shift'))]
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 75))
    check_polygon_selector(event_sequence, expected_result, 1)

    # Move first vertex after completing the polygon.
    expected_result = [(75, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50)
                      + [('onmove', dict(xdata=50, ydata=50)),
                         ('press', dict(xdata=50, ydata=50)),
                         ('onmove', dict(xdata=75, ydata=50)),
                         ('release', dict(xdata=75, ydata=50))])
    check_polygon_selector(event_sequence, expected_result, 2)

    # Move all vertices after completing the polygon.
    expected_result = [(75, 75), (175, 75), (75, 175)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50)
                      + [('on_key_press', dict(key='shift')),
                         ('onmove', dict(xdata=100, ydata=100)),
                         ('press', dict(xdata=100, ydata=100)),
                         ('onmove', dict(xdata=125, ydata=125)),
                         ('release', dict(xdata=125, ydata=125)),
                         ('on_key_release', dict(key='shift'))])
    check_polygon_selector(event_sequence, expected_result, 2)

    # Try to move a vertex and move all before placing any vertices.
    expected_result = [(50, 50), (150, 50), (50, 150)]
    event_sequence = ([('on_key_press', dict(key='control')),
                       ('onmove', dict(xdata=100, ydata=100)),
                       ('press', dict(xdata=100, ydata=100)),
                       ('onmove', dict(xdata=125, ydata=125)),
                       ('release', dict(xdata=125, ydata=125)),
                       ('on_key_release', dict(key='control')),
                       ('on_key_press', dict(key='shift')),
                       ('onmove', dict(xdata=100, ydata=100)),
                       ('press', dict(xdata=100, ydata=100)),
                       ('onmove', dict(xdata=125, ydata=125)),
                       ('release', dict(xdata=125, ydata=125)),
                       ('on_key_release', dict(key='shift'))]
                      + polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50))
    check_polygon_selector(event_sequence, expected_result, 1)

    # Try to place vertex out-of-bounds, then reset, and start a new polygon.
    expected_result = [(50, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(250, 50)
                      + [('on_key_press', dict(key='escape')),
                         ('on_key_release', dict(key='escape'))]
                      + polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50))
    check_polygon_selector(event_sequence, expected_result, 1)
