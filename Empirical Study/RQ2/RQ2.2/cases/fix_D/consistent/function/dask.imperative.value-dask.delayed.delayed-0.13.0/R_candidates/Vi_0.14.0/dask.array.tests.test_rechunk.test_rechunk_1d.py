def test_rechunk_1d():
    """Try rechunking a random 1d matrix"""
    a = np.random.uniform(0, 1, 300)
    x = da.from_array(a, chunks=((100, ) * 3, ))
    new = ((50, ) * 6,)
    x2 = rechunk(x, chunks=new)
    assert x2.chunks == new
    assert np.all(x2.compute() == a)
