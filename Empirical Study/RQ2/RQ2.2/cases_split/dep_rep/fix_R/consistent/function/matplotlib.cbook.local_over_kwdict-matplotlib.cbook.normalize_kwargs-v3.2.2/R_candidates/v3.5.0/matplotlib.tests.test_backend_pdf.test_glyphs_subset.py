def test_glyphs_subset():
    fpath = str(_get_data_path("fonts/ttf/DejaVuSerif.ttf"))
    chars = "these should be subsetted! 1234567890"

    # non-subsetted FT2Font
    nosubfont = FT2Font(fpath)
    nosubfont.set_text(chars)

    # subsetted FT2Font
    subfont = FT2Font(get_glyphs_subset(fpath, chars))
    subfont.set_text(chars)

    nosubcmap = nosubfont.get_charmap()
    subcmap = subfont.get_charmap()

    # all unique chars must be available in subsetted font
    assert set(chars) == set(chr(key) for key in subcmap.keys())

    # subsetted font's charmap should have less entries
    assert len(subcmap) < len(nosubcmap)

    # since both objects are assigned same characters
    assert subfont.get_num_glyphs() == nosubfont.get_num_glyphs()
