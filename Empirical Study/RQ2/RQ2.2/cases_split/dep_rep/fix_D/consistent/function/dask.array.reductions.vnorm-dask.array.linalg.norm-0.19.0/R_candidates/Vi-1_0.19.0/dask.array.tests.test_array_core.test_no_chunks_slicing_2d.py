def test_no_chunks_slicing_2d():
    X = np.arange(24).reshape((4, 6))
    x = da.from_array(X, chunks=(2, 2))
    x._chunks = ((2, 2), (np.nan, np.nan, np.nan))

    assert_eq(x[0], X[0])

    for op in [lambda: x[:, 4],
               lambda: x[:, ::2],
               lambda: x[0, 2:4]]:
        with pytest.raises(ValueError) as e:
            op()
        assert 'chunk' in str(e) and 'unknown' in str(e)
