@pytest.mark.parametrize('shape,limit,expected', [
    (100, 10, (10,) * 10),
    (20, 10, (10, 10)),
    (20, 5, (5, 5, 5, 5)),
    (24, 5, (4, 4, 4, 4, 4, 4)),  # common factor is close, use it
    (23, 5, (5, 5, 5, 5, 3)),  # relatively prime, don't use 1s
    (1000, 167, (125,) * 8),  # find close value
])
def test_normalize_chunks_auto_1d(shape, limit, expected):
    result = normalize_chunks('auto', (shape,), limit=limit * 8, dtype=np.float64)
    assert result == (expected,)
