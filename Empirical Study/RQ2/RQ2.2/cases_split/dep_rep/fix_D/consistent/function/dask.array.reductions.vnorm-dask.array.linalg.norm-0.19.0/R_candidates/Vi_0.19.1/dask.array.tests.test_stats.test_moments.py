@pytest.mark.parametrize('k', range(5))
def test_moments(k):
    x = np.random.random(size=(30, 2))
    y = da.from_array(x, 3)

    expected = scipy.stats.moment(x, k)
    result = dask.array.stats.moment(y, k)
    assert_eq(result, expected)
