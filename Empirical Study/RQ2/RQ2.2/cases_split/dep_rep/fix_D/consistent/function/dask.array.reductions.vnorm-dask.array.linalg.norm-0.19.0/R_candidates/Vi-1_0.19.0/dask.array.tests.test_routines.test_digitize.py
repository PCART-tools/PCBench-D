def test_digitize():
    x = np.array([2, 4, 5, 6, 1])
    bins = np.array([1, 2, 3, 4, 5])
    for chunks in [2, 4]:
        for right in [False, True]:
            d = da.from_array(x, chunks=chunks)
            assert_eq(da.digitize(d, bins, right=right),
                      np.digitize(x, bins, right=right))

    x = np.random.random(size=(100, 100))
    bins = np.random.random(size=13)
    bins.sort()
    for chunks in [(10, 10), (10, 20), (13, 17), (87, 54)]:
        for right in [False, True]:
            d = da.from_array(x, chunks=chunks)
            assert_eq(da.digitize(d, bins, right=right),
                      np.digitize(x, bins, right=right))
