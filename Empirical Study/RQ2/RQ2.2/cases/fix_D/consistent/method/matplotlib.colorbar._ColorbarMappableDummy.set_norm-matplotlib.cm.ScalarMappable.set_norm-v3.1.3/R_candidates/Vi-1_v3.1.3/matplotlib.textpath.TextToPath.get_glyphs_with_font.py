    def get_glyphs_with_font(self, font, s, glyph_map=None,
                             return_new_glyphs_only=False):
        """
        Convert string *s* to vertices and codes using the provided ttf font.
        """

        # Mostly copied from backend_svg.py.

        lastgind = None

        currx = 0
        xpositions = []
        glyph_ids = []

        if glyph_map is None:
            glyph_map = OrderedDict()

        if return_new_glyphs_only:
            glyph_map_new = OrderedDict()
        else:
            glyph_map_new = glyph_map

        # I'm not sure if I get kernings right. Needs to be verified. -JJL

        for c in s:
            ccode = ord(c)
            gind = font.get_char_index(ccode)
            if gind is None:
                ccode = ord('?')
                gind = 0

            if lastgind is not None:
                kern = font.get_kerning(lastgind, gind, KERNING_DEFAULT)
            else:
                kern = 0

            glyph = font.load_char(ccode, flags=LOAD_NO_HINTING)
            horiz_advance = glyph.linearHoriAdvance / 65536

            char_id = self._get_char_id(font, ccode)
            if char_id not in glyph_map:
                glyph_map_new[char_id] = font.get_path()

            currx += kern / 64

            xpositions.append(currx)
            glyph_ids.append(char_id)

            currx += horiz_advance

            lastgind = gind

        ypositions = [0] * len(xpositions)
        sizes = [1.] * len(xpositions)

        rects = []

        return (list(zip(glyph_ids, xpositions, ypositions, sizes)),
                glyph_map_new, rects)
