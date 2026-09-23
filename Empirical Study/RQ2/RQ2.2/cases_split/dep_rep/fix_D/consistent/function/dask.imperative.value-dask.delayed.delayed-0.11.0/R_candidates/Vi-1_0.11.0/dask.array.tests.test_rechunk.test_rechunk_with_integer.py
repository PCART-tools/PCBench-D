def test_rechunk_with_integer():
    x = da.from_array(np.arange(5), chunks=4)
    y = x.rechunk(3)
    assert y.chunks == ((3, 2),)
    assert (x.compute() == y.compute()).all()
