def test_rechunk_4d():
    """Try rechunking a random 4d matrix"""
    old = ((5,5),)*4
    a = np.random.uniform(0,1,10000).reshape((10,) * 4)
    x = da.from_array(a, chunks=old)
    new = ((10,),)* 4
    x2 =rechunk(x, chunks=new)
    assert x2.chunks == new
    assert np.all(x2.compute() == a)
