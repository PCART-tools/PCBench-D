def test_elemwise_on_scalars():
    x = np.arange(10, dtype=np.int64)
    a = from_array(x, chunks=(5,))
    assert len(a.__dask_keys__()) == 2
    assert_eq(a.sum()**2, x.sum()**2)

    y = np.arange(10, dtype=np.int32)
    b = from_array(y, chunks=(5,))
    result = a.sum() * b
    # Dask 0-d arrays do not behave like numpy scalars for type promotion
    assert result.dtype == np.int64
    assert result.compute().dtype == np.int64
    assert (x.sum() * y).dtype == np.int32
    assert_eq((x.sum() * y).astype(np.int64), result)
