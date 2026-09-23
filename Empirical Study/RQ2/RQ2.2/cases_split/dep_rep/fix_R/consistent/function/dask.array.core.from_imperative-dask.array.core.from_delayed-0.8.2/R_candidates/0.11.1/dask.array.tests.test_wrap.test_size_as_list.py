def test_size_as_list():
    a = ones([10, 10], dtype='i4', chunks=(4, 4))
    x = np.array(a)
    assert (x == np.ones((10, 10), dtype='i4')).all()
