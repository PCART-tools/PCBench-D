def test_average_weights():
    a = np.arange(6).reshape((3,2))
    d_a = da.from_array(a, chunks=2)

    weights = np.array([0.25, 0.75])
    d_weights = da.from_array(weights, chunks=2)

    np_avg = np.average(a, weights=weights, axis=1)
    da_avg = da.average(d_a, weights=d_weights, axis=1)

    assert_eq(np_avg, da_avg)
