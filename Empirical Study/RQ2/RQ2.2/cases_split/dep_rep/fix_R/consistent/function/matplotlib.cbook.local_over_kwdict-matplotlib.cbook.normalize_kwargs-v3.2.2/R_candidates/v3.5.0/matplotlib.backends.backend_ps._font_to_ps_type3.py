def _font_to_ps_type3(font_path, chars):
    """
    Subset *chars* from the font at *font_path* into a Type 3 font.

    Parameters
    ----------
    font_path : path-like
        Path to the font to be subsetted.
    chars : str
        The characters to include in the subsetted font.

    Returns
    -------
    str
        The string representation of a Type 3 font, which can be included
        verbatim into a PostScript file.
    """
    font = get_font(font_path, hinting_factor=1)
    glyph_ids = [font.get_char_index(c) for c in chars]

    preamble = """\
%!PS-Adobe-3.0 Resource-Font
%%Creator: Converted from TrueType to Type 3 by Matplotlib.
10 dict begin
/FontName /{font_name} def
/PaintType 0 def
/FontMatrix [{inv_units_per_em} 0 0 {inv_units_per_em} 0 0] def
/FontBBox [{bbox}] def
/FontType 3 def
/Encoding [{encoding}] def
/CharStrings {num_glyphs} dict dup begin
/.notdef 0 def
""".format(font_name=font.postscript_name,
           inv_units_per_em=1 / font.units_per_EM,
           bbox=" ".join(map(str, font.bbox)),
           encoding=" ".join("/{}".format(font.get_glyph_name(glyph_id))
                             for glyph_id in glyph_ids),
           num_glyphs=len(glyph_ids) + 1)
    postamble = """
end readonly def

/BuildGlyph {
 exch begin
 CharStrings exch
 2 copy known not {pop /.notdef} if
 true 3 1 roll get exec
 end
} _d

/BuildChar {
 1 index /Encoding get exch get
 1 index /BuildGlyph get exec
} _d

FontName currentdict end definefont pop
"""

    entries = []
    for glyph_id in glyph_ids:
        g = font.load_glyph(glyph_id, LOAD_NO_SCALE)
        v, c = font.get_path()
        entries.append(
            "/%(name)s{%(bbox)s sc\n" % {
                "name": font.get_glyph_name(glyph_id),
                "bbox": " ".join(map(str, [g.horiAdvance, 0, *g.bbox])),
            }
            + _path.convert_to_string(
                # Convert back to TrueType's internal units (1/64's).
                # (Other dimensions are already in these units.)
                Path(v * 64, c), None, None, False, None, 0,
                # No code for quad Beziers triggers auto-conversion to cubics.
                # Drop intermediate closepolys (relying on the outline
                # decomposer always explicitly moving to the closing point
                # first).
                [b"m", b"l", b"", b"c", b""], True).decode("ascii")
            + "ce} _d"
        )

    return preamble + "\n".join(entries) + postamble
