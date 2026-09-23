def test_sanitize_index():
    pd = pytest.importorskip('pandas')
    with pytest.raises(TypeError):
        sanitize_index('Hello!')

    assert sanitize_index(pd.Series([1, 2, 3])) == [1, 2, 3]
    assert sanitize_index((1, 2, 3)) == [1, 2, 3]
