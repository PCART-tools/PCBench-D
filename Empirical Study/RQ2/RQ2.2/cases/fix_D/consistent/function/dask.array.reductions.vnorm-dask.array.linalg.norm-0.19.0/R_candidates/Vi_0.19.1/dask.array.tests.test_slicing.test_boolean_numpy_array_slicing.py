def test_boolean_numpy_array_slicing():
    with pytest.raises(IndexError):
        da.asarray(range(2))[np.array([True])]
    with pytest.raises(IndexError):
        da.asarray(range(2))[np.array([False, False, False])]
    x = np.arange(5)
    ind = np.array([True, False, False, False, True])
    assert_eq(da.asarray(x)[ind], x[ind])
    # https://github.com/dask/dask/issues/3706
    ind = np.array([True])
    assert_eq(da.asarray([0])[ind], np.arange(1)[ind])
