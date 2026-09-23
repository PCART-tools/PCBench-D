@pytest.mark.skipif(np.__version__ < '1.13.0', reason='array_ufunc not present')
def test_out_numpy():
    x = da.arange(10, chunks=(5,))
    empty = np.empty(10, dtype=x.dtype)
    with pytest.raises((TypeError, NotImplementedError)) as info:
        np.add(x, 1, out=empty)

    assert 'ndarray' in str(info.value)
    assert 'Array' in str(info.value)
