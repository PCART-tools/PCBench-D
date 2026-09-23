def test_normalize_chunks_nan():
    with pytest.raises(ValueError) as info:
        normalize_chunks('auto', (np.nan,), limit=10, dtype=np.uint8)
    assert "auto" in str(info.value)
    with pytest.raises(ValueError) as info:
        normalize_chunks(((np.nan, np.nan), 'auto'), (10, 10), limit=10, dtype=np.uint8)
    assert "auto" in str(info.value)
