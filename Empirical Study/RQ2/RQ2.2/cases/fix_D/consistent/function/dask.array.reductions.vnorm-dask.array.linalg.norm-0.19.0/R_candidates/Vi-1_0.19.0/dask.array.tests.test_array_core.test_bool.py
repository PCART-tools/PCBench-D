def test_bool():
    arr = np.arange(100).reshape((10,10))
    darr = da.from_array(arr, chunks=(10,10))
    with pytest.raises(ValueError):
        bool(darr)
        bool(darr == darr)
