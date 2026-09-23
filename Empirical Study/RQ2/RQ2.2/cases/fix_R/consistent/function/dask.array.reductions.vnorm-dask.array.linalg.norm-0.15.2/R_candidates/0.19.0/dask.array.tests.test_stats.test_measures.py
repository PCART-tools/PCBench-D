@pytest.mark.parametrize('kind, kwargs', [
    ('skew', {}),
    ('kurtosis', {}),
    ('kurtosis', {'fisher': False}),
])
def test_measures(kind, kwargs):
    x = np.random.random(size=(30, 2))
    y = da.from_array(x, 3)
    dfunc = getattr(dask.array.stats, kind)
    sfunc = getattr(scipy.stats, kind)

    expected = sfunc(x, **kwargs)
    result = dfunc(y, **kwargs)
    assert_eq(result, expected)
    assert isinstance(result, da.Array)
