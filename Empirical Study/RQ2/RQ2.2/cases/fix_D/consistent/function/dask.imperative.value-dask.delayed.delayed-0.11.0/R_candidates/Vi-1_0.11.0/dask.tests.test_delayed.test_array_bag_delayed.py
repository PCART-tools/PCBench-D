def test_array_bag_delayed():
    db = pytest.importorskip('dask.bag')
    da = pytest.importorskip('dask.array')
    np = pytest.importorskip('numpy')

    arr1 = np.arange(100).reshape((10, 10))
    arr2 = arr1.dot(arr1.T)
    darr1 = da.from_array(arr1, chunks=(5, 5))
    darr2 = da.from_array(arr2, chunks=(5, 5))
    b = db.from_sequence([1, 2, 3])
    seq = [arr1, arr2, darr1, darr2, b]
    out = delayed(sum)([i.sum() for i in seq])
    assert out.compute() == 2*arr1.sum() + 2*arr2.sum() + sum([1, 2, 3])
