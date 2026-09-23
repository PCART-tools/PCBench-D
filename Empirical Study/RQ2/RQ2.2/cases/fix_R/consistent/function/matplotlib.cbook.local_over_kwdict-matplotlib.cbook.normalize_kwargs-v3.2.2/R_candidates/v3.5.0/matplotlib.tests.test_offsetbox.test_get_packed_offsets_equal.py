@pytest.mark.parametrize('wd_list, total, sep, expected', [
    _Params(  # total larger than required
        [(3, 0), (2, 0), (1, 0)], total=6, sep=None, expected=(6, [0, 2, 4])),
    _Params(  # total smaller sum of widths: overlapping boxes
        [(3, 0), (2, 0), (1, 0), (.5, 0)], total=2, sep=None,
        expected=(2, [0, 0.5, 1, 1.5])),
    _Params(  # total larger than required
        [(.5, 0), (1, 0), (.2, 0)], total=None, sep=1,
        expected=(6, [0, 2, 4])),
    # the case total=None, sep=None is tested separately below
])
def test_get_packed_offsets_equal(wd_list, total, sep, expected):
    result = _get_packed_offsets(wd_list, total, sep, mode='equal')
    assert result[0] == expected[0]
    assert_allclose(result[1], expected[1])
