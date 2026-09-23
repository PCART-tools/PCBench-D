def test_bad_bounds():
    c = [1, 2]
    assert_raises(ValueError, _clean_inputs, c=c, bounds=(1, -2))
    assert_raises(ValueError, _clean_inputs, c=c, bounds=[(1, -2)])
    assert_raises(ValueError, _clean_inputs, c=c, bounds=[(1, -2), (1, 2)])

    assert_raises(ValueError, _clean_inputs, c=c, bounds=(1, 2, 2))
    assert_raises(ValueError, _clean_inputs, c=c, bounds=[(1, 2, 2)])
    assert_raises(ValueError, _clean_inputs, c=c, bounds=[(1, 2), (1, 2, 2)])
    assert_raises(ValueError, _clean_inputs, c=c,
                  bounds=[(1, 2), (1, 2), (1, 2)])
