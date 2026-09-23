def test_map_blocks_block_info():
    x = da.arange(50, chunks=10)

    def func(a, b, c, block_info=None):
        for idx in [0, 2]:  # positions in args
            assert block_info[idx]['shape'] == (50,)
            assert block_info[idx]['num-chunks'] == (5,)
            start, stop = block_info[idx]['array-location'][0]
            assert stop - start == 10
            assert 0 <= start <= 40
            assert 10 <= stop <= 50

            assert 0 <= block_info[idx]['chunk-location'][0] <= 4

        return a + b + c

    z = da.map_blocks(func, x, 100, x + 1, dtype=x.dtype)
    assert_eq(z, x + x + 1 + 100)
