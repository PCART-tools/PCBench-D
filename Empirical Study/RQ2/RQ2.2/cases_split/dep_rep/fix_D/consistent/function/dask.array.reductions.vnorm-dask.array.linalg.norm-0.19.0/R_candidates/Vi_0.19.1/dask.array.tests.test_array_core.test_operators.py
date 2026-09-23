def test_operators():
    x = np.arange(10)
    y = np.arange(10).reshape((10, 1))
    a = from_array(x, chunks=(5,))
    b = from_array(y, chunks=(5, 1))

    c = a + 1
    assert_eq(c, x + 1)

    c = a + b
    assert_eq(c, x + x.reshape((10, 1)))

    expr = (3 / a * b)**2 > 5
    with pytest.warns(None):  # ZeroDivisionWarning
        assert_eq(expr, (3 / x * y)**2 > 5)

    with pytest.warns(None):  # OverflowWarning
        c = da.exp(a)
    assert_eq(c, np.exp(x))

    assert_eq(abs(-a), a)
    assert_eq(a, +x)
