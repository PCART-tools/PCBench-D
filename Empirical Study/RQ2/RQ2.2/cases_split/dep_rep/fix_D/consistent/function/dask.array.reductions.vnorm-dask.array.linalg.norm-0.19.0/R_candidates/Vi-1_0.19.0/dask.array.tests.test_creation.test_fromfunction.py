def test_fromfunction():
    def f(x, y):
        return x + y
    d = da.fromfunction(f, shape=(5, 5), chunks=(2, 2), dtype='f8')

    assert_eq(d, np.fromfunction(f, shape=(5, 5)))
    assert same_keys(d, da.fromfunction(f, shape=(5, 5), chunks=(2, 2), dtype='f8'))
