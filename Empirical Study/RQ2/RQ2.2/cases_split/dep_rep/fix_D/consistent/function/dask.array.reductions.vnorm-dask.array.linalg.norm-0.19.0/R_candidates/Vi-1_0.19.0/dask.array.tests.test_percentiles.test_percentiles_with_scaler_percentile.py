@pytest.mark.parametrize('q', [5, 5.0, np.int64(5), np.float64(5)])
def test_percentiles_with_scaler_percentile(q):
    # Regression test to ensure da.percentile works with scalar percentiles
    # See #3020
    d = da.ones((16,), chunks=(4,))
    assert_eq(da.percentile(d, q), np.array([1], dtype=d.dtype))
