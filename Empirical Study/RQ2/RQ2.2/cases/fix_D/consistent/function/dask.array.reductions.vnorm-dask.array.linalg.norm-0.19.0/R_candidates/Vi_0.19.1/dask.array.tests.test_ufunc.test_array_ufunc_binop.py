@pytest.mark.skipif(np.__version__ < '1.13.0', reason='array_ufunc not present')
def test_array_ufunc_binop():
    x = np.arange(25).reshape((5, 5))
    d = da.from_array(x, chunks=(2, 2))

    for func in [np.add, np.multiply]:
        assert isinstance(func(d, d), da.Array)
        assert_eq(func(d, d), func(x, x))

        assert isinstance(func.outer(d, d), da.Array)
        assert_eq(func.outer(d, d), func.outer(x, x))
