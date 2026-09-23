def test_nonfusible_fancy_indexing():
    nil = slice(None)
    cases = [# x[:, list, :][int, :, :]
             ((nil, [1, 2, 3], nil), (0, nil, nil)),
             # x[int, :, :][:, list, :]
             ((0, nil, nil), (nil, [1, 2, 3], nil)),
             # x[:, list, :, :][:, :, :, int]
             ((nil, [1, 2], nil, nil), (nil, nil, nil, 0))]

    for a, b in cases:
        with pytest.raises(NotImplementedError):
            fuse_slice(a, b)
