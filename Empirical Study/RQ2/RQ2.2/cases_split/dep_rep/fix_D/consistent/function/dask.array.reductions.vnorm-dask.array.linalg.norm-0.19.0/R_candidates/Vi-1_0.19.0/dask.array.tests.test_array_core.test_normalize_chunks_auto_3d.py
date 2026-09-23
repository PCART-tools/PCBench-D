def test_normalize_chunks_auto_3d():
    result = normalize_chunks(('auto', 'auto', 2), (20, 20, 20), limit=200, dtype='uint8')
    expected = ((10, 10), (10, 10), (2,) * 10)
    assert result == expected

    result = normalize_chunks('auto', (20, 20, 20), limit=8, dtype='uint8')
    expected = ((2,) * 10,) * 3
    assert result == expected
