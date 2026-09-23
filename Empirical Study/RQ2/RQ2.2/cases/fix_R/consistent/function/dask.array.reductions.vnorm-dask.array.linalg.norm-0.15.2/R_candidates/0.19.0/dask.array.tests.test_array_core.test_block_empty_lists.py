def test_block_empty_lists():
    for arrays in [
            [],
            [[]],
            [[1], []],
    ]:
        with pytest.raises(ValueError) as e:
            da.block(arrays)
        e.match(r'empty')
