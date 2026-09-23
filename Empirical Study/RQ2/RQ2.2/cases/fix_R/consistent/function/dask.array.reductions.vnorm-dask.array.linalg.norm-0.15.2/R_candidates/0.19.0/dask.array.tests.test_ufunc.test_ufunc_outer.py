def test_ufunc_outer():
    arr1 = np.random.randint(1, 100, size=20)
    darr1 = da.from_array(arr1, 3)

    arr2 = np.random.randint(1, 100, size=(10, 3))
    darr2 = da.from_array(arr2, 3)

    # Check output types
    assert isinstance(da.add.outer(darr1, darr2), da.Array)
    assert isinstance(da.add.outer(arr1, darr2), da.Array)
    assert isinstance(da.add.outer(darr1, arr2), da.Array)
    assert isinstance(da.add.outer(arr1, arr2), np.ndarray)

    # Check mix of dimensions, dtypes, and numpy/dask/object
    cases = [((darr1, darr2), (arr1, arr2)),
             ((darr2, darr1), (arr2, arr1)),
             ((darr2, darr1.astype('f8')), (arr2, arr1.astype('f8'))),
             ((darr1, arr2), (arr1, arr2)),
             ((darr1, 1), (arr1, 1)),
             ((1, darr2), (1, arr2)),
             ((1.5, darr2), (1.5, arr2)),
             (([1, 2, 3], darr2), ([1, 2, 3], arr2)),
             ((darr1.sum(), darr2), (arr1.sum(), arr2)),
             ((np.array(1), darr2), (np.array(1), arr2))]

    for (dA, dB), (A, B) in cases:
        assert_eq(da.add.outer(dA, dB), np.add.outer(A, B))

    # Check dtype kwarg works
    assert_eq(da.add.outer(darr1, darr2, dtype='f8'),
              np.add.outer(arr1, arr2, dtype='f8'))

    with pytest.raises(ValueError):
        da.add.outer(darr1, darr2, out=arr1)

    with pytest.raises(ValueError):
        da.sin.outer(darr1, darr2)
