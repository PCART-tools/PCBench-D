def test_histogram_return_type():
    v = da.random.random(100, chunks=10)
    bins = np.arange(0, 1.01, 0.01)
    # Check if return type is same as hist
    bins = np.arange(0, 11, 1, dtype='i4')
    assert_eq(da.histogram(v * 10, bins=bins)[0],
              np.histogram(v * 10, bins=bins)[0])
