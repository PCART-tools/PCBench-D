def test_where_bool_optimization():
    x = np.random.randint(10, size=(15, 16))
    d = da.from_array(x, chunks=(4, 5))
    y = np.random.randint(10, size=(15, 16))
    e = da.from_array(y, chunks=(4, 5))

    for c in [True, False, np.True_, np.False_, 1, 0]:
        w1 = da.where(c, d, e)
        w2 = np.where(c, x, y)

        assert_eq(w1, w2)

        ex_w1 = d if c else e

        assert w1 is ex_w1
