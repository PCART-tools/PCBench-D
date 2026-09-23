def test_chunksize_too_big_to_chunk(chunk_limit_setup):
    ra, gc, p, idt = chunk_limit_setup
    # set big enough that we do not try to chunk
    rcParams['agg.path.chunksize'] = 1_000_000
    with pytest.raises(OverflowError, match='Please reduce'):
        ra.draw_path(gc, p, idt)
