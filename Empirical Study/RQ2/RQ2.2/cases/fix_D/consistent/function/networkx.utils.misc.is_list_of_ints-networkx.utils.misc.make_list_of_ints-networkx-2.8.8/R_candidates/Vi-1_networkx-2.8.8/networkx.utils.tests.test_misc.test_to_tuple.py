def test_to_tuple():
    a_list = [1, 2, [1, 3]]
    actual = to_tuple(a_list)
    expected = (1, 2, (1, 3))
    assert actual == expected

    a_tuple = (1, 2)
    actual = to_tuple(a_tuple)
    expected = a_tuple
    assert actual == expected

    a_mix = (1, 2, [1, 3])
    actual = to_tuple(a_mix)
    expected = (1, 2, (1, 3))
    assert actual == expected
