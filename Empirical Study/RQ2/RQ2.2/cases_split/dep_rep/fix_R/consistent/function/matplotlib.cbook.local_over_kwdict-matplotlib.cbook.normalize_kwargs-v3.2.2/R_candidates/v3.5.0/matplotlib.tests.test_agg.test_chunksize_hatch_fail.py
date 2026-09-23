def test_chunksize_hatch_fail(chunk_limit_setup):
    ra, gc, p, idt = chunk_limit_setup

    gc.set_hatch('/')

    with pytest.raises(OverflowError, match='hatched path'):
        ra.draw_path(gc, p, idt)
