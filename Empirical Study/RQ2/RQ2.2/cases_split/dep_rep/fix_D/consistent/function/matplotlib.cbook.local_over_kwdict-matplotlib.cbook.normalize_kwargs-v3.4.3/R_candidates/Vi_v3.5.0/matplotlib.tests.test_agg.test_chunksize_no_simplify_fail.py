def test_chunksize_no_simplify_fail(chunk_limit_setup):
    ra, gc, p, idt = chunk_limit_setup
    p.should_simplify = False
    with pytest.raises(OverflowError, match="should_simplify is False"):
        ra.draw_path(gc, p, idt)
