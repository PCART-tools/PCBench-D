def eq(a, b):
    """a is a dask array, b is a numpy array. Checks dtype, shape and value. No
    `assert` needed.
    """
    a = np.array(a)
    assert a.shape == b.shape
    assert a.dtype == b.dtype
    assert_array_almost_equal(a, b)
