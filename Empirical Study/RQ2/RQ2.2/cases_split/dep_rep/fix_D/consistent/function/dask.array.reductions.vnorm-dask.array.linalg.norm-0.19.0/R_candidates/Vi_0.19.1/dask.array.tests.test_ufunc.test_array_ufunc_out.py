@pytest.mark.skipif(np.__version__ < '1.13.0', reason='array_ufunc not present')
def test_array_ufunc_out():
    x = da.arange(10, chunks=(5,))
    np.sin(x, out=x)
    np.add(x, 10, out=x)
    assert_eq(x, np.sin(np.arange(10)) + 10)
