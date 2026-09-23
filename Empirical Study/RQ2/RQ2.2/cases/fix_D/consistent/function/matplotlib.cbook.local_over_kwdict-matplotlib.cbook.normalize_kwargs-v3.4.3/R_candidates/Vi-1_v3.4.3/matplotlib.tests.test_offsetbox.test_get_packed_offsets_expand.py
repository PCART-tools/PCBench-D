@pytest.mark.parametrize('wd_list, total, sep, expected', [
    _Params(  # total=None (implicit 1)
        [(.1, 0)] * 3, total=None, sep=None, expected=(1, [0, .45, .9])),
    _Params(  # total larger than sum of widths
        [(3, 0), (1, 0), (2, 0)], total=10, sep=1, expected=(10, [0, 5, 8])),
    _Params(  # total smaller sum of widths: overlapping boxes
        [(3, 0), (1, 0), (2, 0)], total=5, sep=1, expected=(5, [0, 2.5, 3])),
])
def test_get_packed_offsets_expand(wd_list, total, sep, expected):
    result = _get_packed_offsets(wd_list, total, sep, mode='expand')
    assert result[0] == expected[0]
    assert_allclose(result[1], expected[1])
