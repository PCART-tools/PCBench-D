def test_common_blockdim():
    assert common_blockdim([(5,), (5,)]) == (5,)
    assert common_blockdim([(5,), (2, 3,)]) == (2, 3)
    assert common_blockdim([(5, 5), (2, 3, 5)]) == (2, 3, 5)
    assert common_blockdim([(5, 5), (2, 3, 5)]) == (2, 3, 5)
    assert common_blockdim([(5, 2, 3), (2, 3, 5)]) == (2, 3, 2, 3)

    assert common_blockdim([(1, 2), (2, 1)]) == (1, 1, 1)
    assert common_blockdim([(1, 2, 2), (2, 1, 2), (2, 2, 1)]) == (1, 1, 1, 1, 1)
