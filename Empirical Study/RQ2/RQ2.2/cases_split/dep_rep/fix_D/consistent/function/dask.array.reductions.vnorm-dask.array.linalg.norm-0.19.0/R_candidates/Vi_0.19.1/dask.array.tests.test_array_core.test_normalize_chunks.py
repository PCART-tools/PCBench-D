def test_normalize_chunks():
    assert normalize_chunks(3, (4, 6)) == ((3, 1), (3, 3))
    assert normalize_chunks(((3, 3), (8,)), (6, 8)) == ((3, 3), (8, ))
    assert normalize_chunks((4, 5), (9,)) == ((4, 5), )
    assert normalize_chunks((4, 5), (9, 9)) == ((4, 4, 1), (5, 4))
    assert normalize_chunks(-1, (5, 5)) == ((5,), (5, ))
    assert normalize_chunks((3, -1), (5, 5)) == ((3, 2), (5, ))
    assert normalize_chunks({0: 3}, (5, 5)) == ((3, 2), (5,))
    assert normalize_chunks([[2, 2], [3, 3]]) == ((2, 2), (3, 3))
    assert normalize_chunks(10, (30, 5)), ((10, 10, 10), (5,))
    assert normalize_chunks((), (0, 0)), ((0,), (0,))
    assert normalize_chunks(-1, (0, 3)), ((0,), (3,))
    assert normalize_chunks("auto", shape=(20,), limit=5, dtype='uint8') == \
        ((5, 5, 5, 5),)

    with pytest.raises(ValueError):
        normalize_chunks(((10,), ), (11, ))
    with pytest.raises(ValueError):
        normalize_chunks(((5, ), (5, )), (5, ))
