def test_histogram_extra_args_and_shapes():
    # Check for extra args and shapes
    bins = np.arange(0, 1.01, 0.01)
    v = da.random.random(100, chunks=10)
    data = [(v, bins, da.ones(100, chunks=v.chunks) * 5),
            (da.random.random((50, 50), chunks=10), bins, da.ones((50, 50), chunks=10) * 5)]

    for v, bins, w in data:
        # density
        assert_eq(da.histogram(v, bins=bins, normed=True)[0],
                  np.histogram(v, bins=bins, normed=True)[0])

        # normed
        assert_eq(da.histogram(v, bins=bins, density=True)[0],
                  np.histogram(v, bins=bins, density=True)[0])

        # weights
        assert_eq(da.histogram(v, bins=bins, weights=w)[0],
                  np.histogram(v, bins=bins, weights=w)[0])

        assert_eq(da.histogram(v, bins=bins, weights=w, density=True)[0],
                  da.histogram(v, bins=bins, weights=w, density=True)[0])
