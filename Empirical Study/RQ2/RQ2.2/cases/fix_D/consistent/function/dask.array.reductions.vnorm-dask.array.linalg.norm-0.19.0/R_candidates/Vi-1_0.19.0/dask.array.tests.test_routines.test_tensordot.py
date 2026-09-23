def test_tensordot():
    x = np.arange(400).reshape((20, 20))
    a = da.from_array(x, chunks=(5, 4))
    y = np.arange(200).reshape((20, 10))
    b = da.from_array(y, chunks=(4, 5))

    for axes in [1, (1, 0)]:
        assert_eq(da.tensordot(a, b, axes=axes), np.tensordot(x, y, axes=axes))
        assert_eq(da.tensordot(x, b, axes=axes), np.tensordot(x, y, axes=axes))
        assert_eq(da.tensordot(a, y, axes=axes), np.tensordot(x, y, axes=axes))

    assert same_keys(da.tensordot(a, b, axes=(1, 0)),
                     da.tensordot(a, b, axes=(1, 0)))

    # Increasing number of chunks warning
    with pytest.warns(None if PY2 else da.PerformanceWarning):
        assert not same_keys(da.tensordot(a, b, axes=0),
                             da.tensordot(a, b, axes=1))
