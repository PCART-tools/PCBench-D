def test_new_blockdim():
    assert new_blockdim(20, [5, 5, 5, 5], slice(0, None, 2)) == [3, 2, 3, 2]
