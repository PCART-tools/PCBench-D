@pytest.mark.parametrize('dtype', [None, [('a', 'f4'), ('b', object)]])
def test_meta(dtype):
    a = da.zeros((1,), chunks=(1,))
    assert a._meta.dtype == a.dtype
    assert isinstance(a._meta, np.ndarray)
    assert a.nbytes < 1000
