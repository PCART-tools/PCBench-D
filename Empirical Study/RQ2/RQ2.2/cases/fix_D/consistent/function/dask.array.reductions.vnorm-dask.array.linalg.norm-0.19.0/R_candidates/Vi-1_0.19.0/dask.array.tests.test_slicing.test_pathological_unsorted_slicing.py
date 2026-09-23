def test_pathological_unsorted_slicing():
    x = da.ones(100, chunks=10)

    # [0, 10, 20, ... 90, 1, 11, 21, ... 91, ...]
    index = np.arange(100).reshape(10, 10).ravel(order='F')

    with pytest.warns(da.PerformanceWarning) as info:
        x[index]

    assert '10' in str(info.list[0])
    assert 'out-of-order' in str(info.list[0])
