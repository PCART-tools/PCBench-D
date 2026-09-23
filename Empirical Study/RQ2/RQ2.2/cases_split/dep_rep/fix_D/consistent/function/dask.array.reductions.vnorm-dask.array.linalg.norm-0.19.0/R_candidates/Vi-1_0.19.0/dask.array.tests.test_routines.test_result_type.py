def test_result_type():
    a = da.from_array(np.ones(5, np.float32), chunks=(3,))
    b = da.from_array(np.ones(5, np.int16), chunks=(3,))
    c = da.from_array(np.ones(5, np.int64), chunks=(3,))
    x = np.ones(5, np.float32)
    assert da.result_type(b, c) == np.int64
    assert da.result_type(a, b, c) == np.float64
    assert da.result_type(b, np.float32) == np.float32
    assert da.result_type(b, np.dtype(np.float32)) == np.float32
    assert da.result_type(b, x) == np.float32
    # Effect of scalars depends on their value
    assert da.result_type(1, b) == np.int16
    assert da.result_type(1.0, a) == np.float32
    assert da.result_type(np.int64(1), b) == np.int16
    assert da.result_type(np.ones((), np.int64), b) == np.int16  # 0d array
    assert da.result_type(1e200, a) == np.float64   # 1e200 is too big for float32
    # dask 0d-arrays are NOT treated like scalars
    c = da.from_array(np.ones((), np.float64), chunks=())
    assert da.result_type(a, c) == np.float64
