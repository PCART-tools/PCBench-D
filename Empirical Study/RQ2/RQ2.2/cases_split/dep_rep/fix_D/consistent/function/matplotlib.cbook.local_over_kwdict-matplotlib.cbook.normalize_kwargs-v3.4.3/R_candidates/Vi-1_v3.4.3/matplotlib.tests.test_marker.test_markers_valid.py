@pytest.mark.parametrize('marker', [
    'o',
    'x',
    '',
    'None',
    None,
    r'$\frac{1}{2}$',
    "$\u266B$",
    1,
    markers.TICKLEFT,
    [[-1, 0], [1, 0]],
    np.array([[-1, 0], [1, 0]]),
    Path([[0, 0], [1, 0]], [Path.MOVETO, Path.LINETO]),
    (5, 0),  # a pentagon
    (7, 1),  # a 7-pointed star
    (5, 2),  # asterisk
    (5, 0, 10),  # a pentagon, rotated by 10 degrees
    (7, 1, 10),  # a 7-pointed star, rotated by 10 degrees
    (5, 2, 10),  # asterisk, rotated by 10 degrees
    markers.MarkerStyle(),
    markers.MarkerStyle('o'),
])
def test_markers_valid(marker):
    # Checking this doesn't fail.
    markers.MarkerStyle(marker)
