def test_chunksize_zero(chunk_limit_setup):
    ra, gc, p, idt = chunk_limit_setup
    # set to zero to disable, currently defaults to 0, but lets be sure
    rcParams['agg.path.chunksize'] = 0
    with pytest.raises(OverflowError, match='Please set'):
        ra.draw_path(gc, p, idt)
