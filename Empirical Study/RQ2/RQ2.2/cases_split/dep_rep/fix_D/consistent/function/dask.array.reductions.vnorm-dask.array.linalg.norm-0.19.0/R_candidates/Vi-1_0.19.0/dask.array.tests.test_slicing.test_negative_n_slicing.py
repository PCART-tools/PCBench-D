def test_negative_n_slicing():
    assert_eq(da.ones(2, chunks=2)[-2], np.ones(2)[-2])
