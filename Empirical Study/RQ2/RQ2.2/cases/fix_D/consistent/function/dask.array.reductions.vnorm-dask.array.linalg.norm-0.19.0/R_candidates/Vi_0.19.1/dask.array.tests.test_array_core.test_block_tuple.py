def test_block_tuple():
    for arrays in [
            ([1, 2], [3, 4]),
            [(1, 2), (3, 4)],
    ]:
        with pytest.raises(TypeError) as e:
            da.block(arrays)
        e.match(r'tuple')
