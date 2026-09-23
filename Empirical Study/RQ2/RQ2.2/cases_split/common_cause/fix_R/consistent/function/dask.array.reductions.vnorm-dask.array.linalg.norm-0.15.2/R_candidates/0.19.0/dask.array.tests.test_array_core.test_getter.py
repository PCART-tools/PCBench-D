def test_getter():
    assert type(getter(np.matrix([[1]]), 0)) is np.ndarray
    assert type(getter(np.matrix([[1]]), 0, asarray=False)) is np.matrix
    assert_eq(getter([1, 2, 3, 4, 5], slice(1, 4)), np.array([2, 3, 4]))

    assert_eq(getter(np.arange(5), (None, slice(None, None))),
              np.arange(5)[None, :])
