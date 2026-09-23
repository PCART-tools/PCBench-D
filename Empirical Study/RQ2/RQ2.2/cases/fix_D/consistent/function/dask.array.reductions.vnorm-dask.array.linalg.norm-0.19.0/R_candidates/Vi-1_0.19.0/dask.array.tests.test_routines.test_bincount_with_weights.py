def test_bincount_with_weights():
    x = np.array([2, 1, 5, 2, 1])
    d = da.from_array(x, chunks=2)
    weights = np.array([1, 2, 1, 0.5, 1])

    dweights = da.from_array(weights, chunks=2)
    e = da.bincount(d, weights=dweights, minlength=6)
    assert_eq(e, np.bincount(x, weights=dweights, minlength=6))
    assert same_keys(da.bincount(d, weights=dweights, minlength=6), e)
