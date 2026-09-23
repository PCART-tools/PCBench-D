def test_elemwise_dtype():
    values = [
        da.from_array(np.ones(5, np.float32), chunks=3),
        da.from_array(np.ones(5, np.int16), chunks=3),
        da.from_array(np.ones(5, np.int64), chunks=3),
        da.from_array(np.ones((), np.float64), chunks=()) * 1e200,
        np.ones(5, np.float32),
        1, 1.0, 1e200, np.int64(1), np.ones((), np.int64),
    ]
    for x in values:
        for y in values:
            assert da.maximum(x, y).dtype == da.result_type(x, y)
