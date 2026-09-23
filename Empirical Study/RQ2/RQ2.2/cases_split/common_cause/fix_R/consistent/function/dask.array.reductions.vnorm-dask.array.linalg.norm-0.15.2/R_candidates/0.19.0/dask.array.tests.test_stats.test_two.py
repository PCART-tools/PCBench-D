@pytest.mark.parametrize('kind, kwargs', [
    ('ttest_ind', {}),
    ('ttest_ind', {'equal_var': False}),
    ('ttest_1samp', {}),
    ('ttest_rel', {}),
    ('chisquare', {}),
    ('power_divergence', {}),
    ('power_divergence', {'lambda_': 0}),
    ('power_divergence', {'lambda_': -1}),
    ('power_divergence', {'lambda_': 'neyman'}),
])
def test_two(kind, kwargs):
    a = np.random.random(size=30,)
    b = np.random.random(size=30,)
    a_ = da.from_array(a, 3)
    b_ = da.from_array(b, 3)

    dask_test = getattr(dask.array.stats, kind)
    scipy_test = getattr(scipy.stats, kind)

    with pytest.warns(None):  # maybe overflow warning (powrer_divergence)
        result = dask_test(a_, b_, **kwargs)
        expected = scipy_test(a, b, **kwargs)

    assert isinstance(result, Delayed)
    assert allclose(result.compute(), expected)
