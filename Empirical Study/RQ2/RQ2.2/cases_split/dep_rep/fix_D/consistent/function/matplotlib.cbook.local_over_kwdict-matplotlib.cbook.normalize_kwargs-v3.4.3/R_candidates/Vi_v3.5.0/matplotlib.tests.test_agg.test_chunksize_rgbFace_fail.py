def test_chunksize_rgbFace_fail(chunk_limit_setup):
    ra, gc, p, idt = chunk_limit_setup

    with pytest.raises(OverflowError, match='filled path'):
        ra.draw_path(gc, p, idt, (1, 0, 0))
