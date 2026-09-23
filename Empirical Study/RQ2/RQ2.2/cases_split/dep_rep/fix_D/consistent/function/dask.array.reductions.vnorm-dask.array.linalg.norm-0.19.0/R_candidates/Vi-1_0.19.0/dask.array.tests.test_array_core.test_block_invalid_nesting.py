def test_block_invalid_nesting():
    for arrays in [
            [1, [2]],
            [1, []],
            [[1], 2],
            [[], 2],
            [
                [[1], [2]],
                [[3, 4]],
                [5]  # missing brackets
            ],
    ]:
        with pytest.raises(ValueError) as e:
            da.block(arrays)
        e.match(r'depths are mismatched')
