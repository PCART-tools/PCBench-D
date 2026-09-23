def test_histogram_alternative_bins_range():
    v = da.random.random(100, chunks=10)
    (a1, b1) = da.histogram(v, bins=10, range=(0, 1))
    (a2, b2) = np.histogram(v, bins=10, range=(0, 1))
    assert_eq(a1, a2)
    assert_eq(b1, b2)
