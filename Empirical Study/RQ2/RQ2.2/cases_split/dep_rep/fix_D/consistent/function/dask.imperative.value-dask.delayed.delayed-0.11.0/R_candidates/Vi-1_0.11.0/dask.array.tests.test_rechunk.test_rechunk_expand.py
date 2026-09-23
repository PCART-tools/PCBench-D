def test_rechunk_expand():
    a = np.random.uniform(0,1,100).reshape((10, 10))
    x = da.from_array(a, chunks=(5, 5))
    y = x.rechunk(chunks=((3, 3, 3, 1), (3, 3, 3, 1)))
    assert np.all(y.compute() == a)
