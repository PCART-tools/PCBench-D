def test_piecewise():
    np.random.seed(1337)

    x = np.random.randint(10, size=(15, 16))
    d = da.from_array(x, chunks=(4, 5))

    assert_eq(
        np.piecewise(x, [x < 5, x >= 5], [lambda e, v, k: e + 1, 5], 1, k=2),
        da.piecewise(d, [d < 5, d >= 5], [lambda e, v, k: e + 1, 5], 1, k=2)
    )
