def test_map_blocks_name():
    assert da.ones(5, chunks=2).map_blocks(inc).name.startswith('inc-')
