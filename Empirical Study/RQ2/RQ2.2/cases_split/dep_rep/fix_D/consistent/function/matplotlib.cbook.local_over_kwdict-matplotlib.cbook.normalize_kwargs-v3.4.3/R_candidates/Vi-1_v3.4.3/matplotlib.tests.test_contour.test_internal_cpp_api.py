@pytest.mark.parametrize("args, cls, message", [
    ((), TypeError,
     'function takes exactly 6 arguments (0 given)'),
    ((1, 2, 3, 4, 5, 6), ValueError,
     'Expected 2-dimensional array, got 0'),
    (([[0]], [[0]], [[]], None, True, 0), ValueError,
     'x, y and z must all be 2D arrays with the same dimensions'),
    (([[0]], [[0]], [[0]], None, True, 0), ValueError,
     'x, y and z must all be at least 2x2 arrays'),
    ((*[np.arange(4).reshape((2, 2))] * 3, [[0]], True, 0), ValueError,
     'If mask is set it must be a 2D array with the same dimensions as x.'),
])
def test_internal_cpp_api(args, cls, message):  # Github issue 8197.
    from matplotlib import _contour  # noqa: ensure lazy-loaded module *is* loaded.
    with pytest.raises(cls, match=re.escape(message)):
        mpl._contour.QuadContourGenerator(*args)
