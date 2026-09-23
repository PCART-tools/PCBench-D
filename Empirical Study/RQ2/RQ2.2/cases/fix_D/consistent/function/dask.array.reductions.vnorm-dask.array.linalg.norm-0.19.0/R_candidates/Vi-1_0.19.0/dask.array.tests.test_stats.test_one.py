@pytest.mark.parametrize('kind', [
    'chisquare', 'power_divergence', 'normaltest', 'skewtest', 'kurtosistest',
])
def test_one(kind):
    a = np.random.random(size=30,)
    a_ = da.from_array(a, 3)

    dask_test = getattr(dask.array.stats, kind)
    scipy_test = getattr(scipy.stats, kind)

    result = dask_test(a_)
    expected = scipy_test(a)

    assert isinstance(result, Delayed)
    assert allclose(result.compute(), expected)
