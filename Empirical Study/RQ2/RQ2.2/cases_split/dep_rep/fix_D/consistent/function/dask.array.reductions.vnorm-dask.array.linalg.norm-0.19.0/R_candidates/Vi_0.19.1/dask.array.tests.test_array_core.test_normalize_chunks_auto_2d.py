@pytest.mark.parametrize('shape,chunks,limit,expected', [
    ((20, 20), ('auto', 2), 20, ((10, 10), (2,) * 10)),
    ((20, 20), ('auto', (2, 2, 2, 2, 2, 5, 5)), 20, ((4, 4, 4, 4, 4), (2, 2, 2, 2, 2, 5, 5))),
    ((1, 20), 'auto', 10, ((1,), (10, 10))),
])
def test_normalize_chunks_auto_2d(shape, chunks, limit, expected):
    result = normalize_chunks(chunks, shape, limit=limit, dtype='uint8')
    assert result == expected
