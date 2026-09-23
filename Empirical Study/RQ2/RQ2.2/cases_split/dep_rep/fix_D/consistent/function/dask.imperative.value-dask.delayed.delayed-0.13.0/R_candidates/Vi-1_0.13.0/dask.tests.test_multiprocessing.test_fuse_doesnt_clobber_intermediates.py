def test_fuse_doesnt_clobber_intermediates():
    d = {'x': 1, 'y': (inc, 'x'), 'z': (add, 10, 'y')}
    assert get(d, ['y', 'z']) == (2, 12)
