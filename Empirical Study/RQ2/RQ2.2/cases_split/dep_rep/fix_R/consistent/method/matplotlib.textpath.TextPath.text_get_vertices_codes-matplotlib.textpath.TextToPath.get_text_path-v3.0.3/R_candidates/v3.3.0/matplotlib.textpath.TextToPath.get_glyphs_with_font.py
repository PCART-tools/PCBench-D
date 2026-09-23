    def get_glyphs_with_font(self, font, s, glyph_map=None,
                             return_new_glyphs_only=False):
        """
        Convert string *s* to vertices and codes using the provided ttf font.
        """

        if glyph_map is None:
            glyph_map = OrderedDict()

        if return_new_glyphs_only:
            glyph_map_new = OrderedDict()
        else:
            glyph_map_new = glyph_map

        xpositions = []
        glyph_ids = []
        for char, (_, x) in zip(s, _text_layout.layout(s, font)):
            char_id = self._get_char_id(font, ord(char))
            glyph_ids.append(char_id)
            xpositions.append(x)
            if char_id not in glyph_map:
                glyph_map_new[char_id] = font.get_path()

        ypositions = [0] * len(xpositions)
        sizes = [1.] * len(xpositions)

        rects = []

        return (list(zip(glyph_ids, xpositions, ypositions, sizes)),
                glyph_map_new, rects)
