@pytest.mark.skipif(np.__version__ < '1.13.0', reason='array_ufunc not present')
def test_unsupported_ufunc_methods():
    x = da.arange(10, chunks=(5,))
    with pytest.raises(TypeError):
        assert np.add.reduce(x)
