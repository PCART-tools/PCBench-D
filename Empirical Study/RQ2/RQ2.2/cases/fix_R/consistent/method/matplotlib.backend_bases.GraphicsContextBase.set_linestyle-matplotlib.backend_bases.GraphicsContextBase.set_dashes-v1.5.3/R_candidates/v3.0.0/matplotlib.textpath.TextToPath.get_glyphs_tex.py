    def get_glyphs_tex(self, prop, s, glyph_map=None,
                       return_new_glyphs_only=False):
        """
        convert the string *s* to vertices and codes using matplotlib's usetex
        mode.
        """

        # codes are modstly borrowed from pdf backend.

        texmanager = self.get_texmanager()

        fontsize = prop.get_size_in_points()
        if hasattr(texmanager, "get_dvi"):
            dvifilelike = texmanager.get_dvi(s, self.FONT_SCALE)
            dvi = dviread.DviFromFileLike(dvifilelike, self.DPI)
        else:
            dvifile = texmanager.make_dvi(s, self.FONT_SCALE)
            dvi = dviread.Dvi(dvifile, self.DPI)
        with dvi:
            page = next(iter(dvi))

        if glyph_map is None:
            glyph_map = OrderedDict()

        if return_new_glyphs_only:
            glyph_map_new = OrderedDict()
        else:
            glyph_map_new = glyph_map

        glyph_ids, xpositions, ypositions, sizes = [], [], [], []

        # Gather font information and do some setup for combining
        # characters into strings.
        # oldfont, seq = None, []
        for x1, y1, dvifont, glyph, width in page.text:
            font, enc = self._get_ps_font_and_encoding(dvifont.texname)
            char_id = self._get_char_id_ps(font, glyph)

            if char_id not in glyph_map:
                font.clear()
                font.set_size(self.FONT_SCALE, self.DPI)
                if enc:
                    charcode = enc.get(glyph, None)
                else:
                    charcode = glyph

                ft2font_flag = LOAD_TARGET_LIGHT
                if charcode is not None:
                    glyph0 = font.load_char(charcode, flags=ft2font_flag)
                else:
                    warnings.warn("The glyph (%d) of font (%s) cannot be "
                                  "converted with the encoding. Glyph may "
                                  "be wrong" % (glyph, font.fname))

                    glyph0 = font.load_char(glyph, flags=ft2font_flag)

                glyph_map_new[char_id] = self.glyph_to_path(font)

            glyph_ids.append(char_id)
            xpositions.append(x1)
            ypositions.append(y1)
            sizes.append(dvifont.size / self.FONT_SCALE)

        myrects = []

        for ox, oy, h, w in page.boxes:
            vert1 = [(ox, oy), (ox + w, oy), (ox + w, oy + h),
                     (ox, oy + h), (ox, oy), (0, 0)]
            code1 = [Path.MOVETO,
                     Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO,
                     Path.CLOSEPOLY]
            myrects.append((vert1, code1))

        return (list(zip(glyph_ids, xpositions, ypositions, sizes)),
                glyph_map_new, myrects)
