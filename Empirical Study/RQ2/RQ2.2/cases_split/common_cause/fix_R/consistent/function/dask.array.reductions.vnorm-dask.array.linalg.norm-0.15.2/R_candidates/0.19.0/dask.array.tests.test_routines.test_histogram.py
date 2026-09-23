def test_histogram():
    # Test for normal, flattened input
    n = 100
    v = da.random.random(n, chunks=10)
    bins = np.arange(0, 1.01, 0.01)
    (a1, b1) = da.histogram(v, bins=bins)
    (a2, b2) = np.histogram(v, bins=bins)

    # Check if the sum of the bins equals the number of samples
    assert a2.sum(axis=0) == n
    assert a1.sum(axis=0) == n
    assert_eq(a1, a2)
    assert same_keys(da.histogram(v, bins=bins)[0], a1)
