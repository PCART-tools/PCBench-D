def test_chunksize_toobig_chunks(chunk_limit_setup):
    ra, gc, p, idt = chunk_limit_setup
    # small enough we will try to chunk, but big enough we will fail
    # to render
    rcParams['agg.path.chunksize'] = 90_000
    with pytest.raises(OverflowError, match='Please reduce'):
        ra.draw_path(gc, p, idt)
