def test_normalize_chunks_tuples_of_tuples():
    result = normalize_chunks(((2, 3, 5), 'auto'), (10, 10), limit=10, dtype=np.uint8)
    expected = ((2, 3, 5), (2, 2, 2, 2, 2))
    assert result == expected
