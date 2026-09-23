def test_bias_raises():
    x = np.random.random(size=(30, 2))
    y = da.from_array(x, 3)

    with pytest.raises(NotImplementedError):
        dask.array.stats.skew(y, bias=False)

    with pytest.raises(NotImplementedError):
        dask.array.stats.kurtosis(y, bias=False)
