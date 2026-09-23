def test_rechunk_1d():
    """Try rechunking a random 1d matrix"""
    a = np.random.uniform(0, 1, 30)
    x = da.from_array(a, chunks=((10, ) * 3, ))
    new = ((5, ) * 6,)
    x2 = rechunk(x, chunks=new)
    assert x2.chunks == new
    assert np.all(x2.compute() == a)
