@pytest.mark.skipif(np.__version__ < '1.13.0', reason='array_ufunc not present')
def test_out_shape_mismatch():
    x = da.arange(10, chunks=(5,))
    y = da.arange(15, chunks=(5,))
    with pytest.raises(ValueError):
        assert np.log(x, out=y)
