def test_power_divergence_invalid():
    a = np.random.random(size=30,)
    a_ = da.from_array(a, 3)

    with pytest.raises(ValueError):
        dask.array.stats.power_divergence(a_, lambda_='wrong')
