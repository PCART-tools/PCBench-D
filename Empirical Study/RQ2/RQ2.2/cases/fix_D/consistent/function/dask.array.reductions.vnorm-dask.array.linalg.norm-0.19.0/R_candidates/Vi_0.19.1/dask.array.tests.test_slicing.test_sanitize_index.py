def test_sanitize_index():
    pd = pytest.importorskip('pandas')
    with pytest.raises(TypeError):
        sanitize_index('Hello!')

    np.testing.assert_equal(sanitize_index(pd.Series([1, 2, 3])), [1, 2, 3])
    np.testing.assert_equal(sanitize_index((1, 2, 3)), [1, 2, 3])
