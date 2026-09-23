@pytest.mark.parametrize('wd_list, total, sep, expected', [
    _Params(  # total=None
        [(3, 0), (1, 0), (2, 0)], total=None, sep=1, expected=(8, [0, 4, 6])),
    _Params(  # total larger than required
        [(3, 0), (1, 0), (2, 0)], total=10, sep=1, expected=(10, [0, 4, 6])),
    _Params(  # total smaller than required
        [(3, 0), (1, 0), (2, 0)], total=5, sep=1, expected=(5, [0, 4, 6])),
])
def test_get_packed_offsets_fixed(wd_list, total, sep, expected):
    result = _get_packed_offsets(wd_list, total, sep, mode='fixed')
    assert result[0] == expected[0]
    assert_allclose(result[1], expected[1])
