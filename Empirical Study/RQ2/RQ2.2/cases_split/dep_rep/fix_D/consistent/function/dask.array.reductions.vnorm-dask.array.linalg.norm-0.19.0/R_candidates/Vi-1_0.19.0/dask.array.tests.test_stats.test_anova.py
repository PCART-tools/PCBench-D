def test_anova():
    np_args = [i * np.random.random(size=(30,)) for i in range(4)]
    da_args = [da.from_array(x, chunks=10) for x in np_args]

    result = dask.array.stats.f_oneway(*da_args)
    expected = scipy.stats.f_oneway(*np_args)

    assert allclose(result.compute(), expected)
