def test_where():
    x = np.random.randint(10, size=(15, 14))
    x[5, 5] = x[4, 4] = 0 # Ensure some false elements
    d = da.from_array(x, chunks=(4, 5))
    y = np.random.randint(10, size=15).astype(np.uint8)
    e = da.from_array(y, chunks=(4,))

    for c1, c2 in [(d > 5, x > 5),
                   (d, x),
                   (1, 1),
                   (0, 0),
                   (5, 5),
                   (True, True),
                   (np.True_, np.True_),
                   (False, False),
                   (np.False_, np.False_)]:
        for b1, b2 in [(0, 0), (-e[:, None], -y[:, None]), (e[:14], y[:14])]:
            w1 = da.where(c1, d, b1)
            w2 = np.where(c2, x, b2)
            assert_eq(w1, w2)
