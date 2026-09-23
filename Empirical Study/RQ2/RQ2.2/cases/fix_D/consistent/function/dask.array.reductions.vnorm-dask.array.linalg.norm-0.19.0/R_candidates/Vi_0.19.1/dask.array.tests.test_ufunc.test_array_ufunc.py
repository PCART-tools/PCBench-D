@pytest.mark.skipif(np.__version__ < '1.13.0', reason='array_ufunc not present')
def test_array_ufunc():
    x = np.arange(24).reshape((4, 6))
    d = da.from_array(x, chunks=(2, 3))

    for func in [np.sin, np.isreal, np.sum, np.negative, partial(np.prod, axis=0)]:
        assert isinstance(func(d), da.Array)
        assert_eq(func(d), func(x))
