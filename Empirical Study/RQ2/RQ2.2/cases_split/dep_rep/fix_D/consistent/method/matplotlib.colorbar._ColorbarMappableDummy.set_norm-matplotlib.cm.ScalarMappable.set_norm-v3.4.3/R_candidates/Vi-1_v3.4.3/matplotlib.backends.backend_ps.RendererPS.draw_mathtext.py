    def draw_mathtext(self, gc, x, y, s, prop, angle):
        """Draw the math text using matplotlib.mathtext."""
        if debugPS:
            self._pswriter.write("% mathtext\n")

        width, height, descent, glyphs, rects = \
            self._text2path.mathtext_parser.parse(
                s, 72, prop,
                _force_standard_ps_fonts=mpl.rcParams["ps.useafm"])
        self.set_color(*gc.get_rgb())
        self._pswriter.write(
            f"gsave\n"
            f"{x:f} {y:f} translate\n"
            f"{angle:f} rotate\n")
        lastfont = None
        for font, fontsize, num, ox, oy in glyphs:
            self._character_tracker.track(font, chr(num))
            if (font.postscript_name, fontsize) != lastfont:
                lastfont = font.postscript_name, fontsize
                self._pswriter.write(
                    f"/{font.postscript_name} {fontsize} selectfont\n")
            symbol_name = (
                font.get_name_char(chr(num)) if isinstance(font, AFM) else
                font.get_glyph_name(font.get_char_index(num)))
            self._pswriter.write(
                f"{ox:f} {oy:f} moveto\n"
                f"/{symbol_name} glyphshow\n")
        for ox, oy, w, h in rects:
            self._pswriter.write(f"{ox} {oy} {w} {h} rectfill\n")
        self._pswriter.write("grestore\n")
