def test_singleton_size():
    a = ones(10, dtype='i4', chunks=(4,))
    x = np.array(a)
    assert (x == np.ones(10, dtype='i4')).all()
