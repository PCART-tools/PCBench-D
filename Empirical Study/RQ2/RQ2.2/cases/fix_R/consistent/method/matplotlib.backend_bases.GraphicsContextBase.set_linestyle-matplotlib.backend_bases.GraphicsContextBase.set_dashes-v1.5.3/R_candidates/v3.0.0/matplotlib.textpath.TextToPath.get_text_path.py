    def get_text_path(self, prop, s, ismath=False, usetex=False):
        """
        convert text *s* to path (a tuple of vertices and codes for
        matplotlib.path.Path).

        *prop*
          font property

        *s*
          text to be converted

        *usetex*
          If True, use matplotlib usetex mode.

        *ismath*
          If True, use mathtext parser. Effective only if usetex == False.


        """
        if not usetex:
            if not ismath:
                font = self._get_font(prop)
                glyph_info, glyph_map, rects = self.get_glyphs_with_font(
                                                    font, s)
            else:
                glyph_info, glyph_map, rects = self.get_glyphs_mathtext(
                                                    prop, s)
        else:
            glyph_info, glyph_map, rects = self.get_glyphs_tex(prop, s)

        verts, codes = [], []

        for glyph_id, xposition, yposition, scale in glyph_info:
            verts1, codes1 = glyph_map[glyph_id]
            if len(verts1):
                verts1 = np.array(verts1) * scale + [xposition, yposition]
                verts.extend(verts1)
                codes.extend(codes1)

        for verts1, codes1 in rects:
            verts.extend(verts1)
            codes.extend(codes1)

        return verts, codes
