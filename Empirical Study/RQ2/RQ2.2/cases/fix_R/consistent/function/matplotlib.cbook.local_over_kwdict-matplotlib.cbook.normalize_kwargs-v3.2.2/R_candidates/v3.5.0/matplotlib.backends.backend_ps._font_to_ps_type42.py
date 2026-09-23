def _font_to_ps_type42(font_path, chars, fh):
    """
    Subset *chars* from the font at *font_path* into a Type 42 font at *fh*.

    Parameters
    ----------
    font_path : path-like
        Path to the font to be subsetted.
    chars : str
        The characters to include in the subsetted font.
    fh : file-like
        Where to write the font.
    """
    subset_str = ''.join(chr(c) for c in chars)
    _log.debug("SUBSET %s characters: %s", font_path, subset_str)
    try:
        fontdata = _backend_pdf_ps.get_glyphs_subset(font_path, subset_str)
        _log.debug("SUBSET %s %d -> %d", font_path, os.stat(font_path).st_size,
                   fontdata.getbuffer().nbytes)

        # Give ttconv a subsetted font along with updated glyph_ids.
        font = FT2Font(fontdata)
        glyph_ids = [font.get_char_index(c) for c in chars]
        with TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, "tmp.ttf")

            with open(tmpfile, 'wb') as tmp:
                tmp.write(fontdata.getvalue())

            # TODO: allow convert_ttf_to_ps to input file objects (BytesIO)
            convert_ttf_to_ps(os.fsencode(tmpfile), fh, 42, glyph_ids)
    except RuntimeError:
        _log.warning(
            "The PostScript backend does not currently "
            "support the selected font.")
        raise
