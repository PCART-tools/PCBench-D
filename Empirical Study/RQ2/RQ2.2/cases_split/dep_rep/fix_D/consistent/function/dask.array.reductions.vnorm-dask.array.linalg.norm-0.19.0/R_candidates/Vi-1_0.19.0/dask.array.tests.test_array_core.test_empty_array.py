def test_empty_array():
    assert_eq(np.arange(0), da.arange(0, chunks=5))
