def test_ones():
    a = ones((10, 10), dtype='i4', chunks=(4, 4))
    x = np.array(a)
    assert (x == np.ones((10, 10), 'i4')).all()
