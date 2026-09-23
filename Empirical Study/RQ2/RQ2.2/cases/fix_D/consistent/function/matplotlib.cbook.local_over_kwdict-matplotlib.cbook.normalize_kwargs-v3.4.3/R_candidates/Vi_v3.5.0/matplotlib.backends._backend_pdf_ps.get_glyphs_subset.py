def get_glyphs_subset(fontfile, characters):
    """
    Subset a TTF font

    Reads the named fontfile and restricts the font to the characters.
    Returns a serialization of the subset font as file-like object.

    Parameters
    ----------
    symbol : str
        Path to the font file
    characters : str
        Continuous set of characters to include in subset
    """

    options = subset.Options(glyph_names=True, recommended_glyphs=True)

    # prevent subsetting FontForge Timestamp and other tables
    options.drop_tables += ['FFTM', 'PfEd']

    with subset.load_font(fontfile, options) as font:
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(text=characters)
        subsetter.subset(font)
        fh = BytesIO()
        font.save(fh, reorderTables=False)
        return fh
