def test_rechunk_2d():
    """Try rechunking a random 2d matrix"""
    a = np.random.uniform(0, 1, 300).reshape((10, 30))
    x = da.from_array(a, chunks=((1, 2, 3, 4), (5, ) * 6))
    new = ((5, 5), (15, ) * 2)
    x2 = rechunk(x, chunks=new)
    assert x2.chunks == new
    assert np.all(x2.compute() == a)
