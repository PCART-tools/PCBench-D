@pytest.mark.parametrize(
    'params, expected_result',
    [(_params(),
      _result(c='b', colors=np.array([[0, 0, 1, 1]]))),
     (_params(c='r'),
      _result(c='r', colors=np.array([[1, 0, 0, 1]]))),
     (_params(c='r', colors='b'),
      _result(c='r', colors=np.array([[1, 0, 0, 1]]))),
     # color
     (_params(color='b'),
      _result(c='b', colors=np.array([[0, 0, 1, 1]]))),
     (_params(color=['b', 'g']),
      _result(c=['b', 'g'], colors=np.array([[0, 0, 1, 1], [0, .5, 0, 1]]))),
     ])
def test_parse_scatter_color_args(params, expected_result):
    def get_next_color():
        return 'blue'  # currently unused

    c, colors, _edgecolors = mpl.axes.Axes._parse_scatter_color_args(
        *params, get_next_color_func=get_next_color)
    assert c == expected_result.c
    assert_allclose(colors, expected_result.colors)
