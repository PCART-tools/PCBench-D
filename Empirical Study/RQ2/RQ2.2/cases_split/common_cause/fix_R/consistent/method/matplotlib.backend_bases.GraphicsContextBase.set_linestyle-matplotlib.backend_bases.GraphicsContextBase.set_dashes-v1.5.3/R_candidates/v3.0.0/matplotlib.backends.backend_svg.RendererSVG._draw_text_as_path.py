    def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath, mtext=None):
        """
        draw the text by converting them to paths using textpath module.

        Parameters
        ----------
        prop : `matplotlib.font_manager.FontProperties`
          font property

        s : str
          text to be converted

        usetex : bool
          If True, use matplotlib usetex mode.

        ismath : bool
          If True, use mathtext parser. If "TeX", use *usetex* mode.

        """
        writer = self.writer

        writer.comment(s)

        glyph_map=self._glyph_map

        text2path = self._text2path
        color = rgb2hex(gc.get_rgb())
        fontsize = prop.get_size_in_points()

        style = {}
        if color != '#000000':
            style['fill'] = color

        alpha = gc.get_alpha() if gc.get_forced_alpha() else gc.get_rgb()[3]
        if alpha != 1:
            style['opacity'] = short_float_fmt(alpha)

        if not ismath:
            font = text2path._get_font(prop)
            _glyphs = text2path.get_glyphs_with_font(
                font, s, glyph_map=glyph_map, return_new_glyphs_only=True)
            glyph_info, glyph_map_new, rects = _glyphs

            if glyph_map_new:
                writer.start('defs')
                for char_id, glyph_path in glyph_map_new.items():
                    path = Path(*glyph_path)
                    path_data = self._convert_path(path, simplify=False)
                    writer.element('path', id=char_id, d=path_data)
                writer.end('defs')

                glyph_map.update(glyph_map_new)

            attrib = {}
            attrib['style'] = generate_css(style)
            font_scale = fontsize / text2path.FONT_SCALE
            attrib['transform'] = generate_transform([
                ('translate', (x, y)),
                ('rotate', (-angle,)),
                ('scale', (font_scale, -font_scale))])

            writer.start('g', attrib=attrib)
            for glyph_id, xposition, yposition, scale in glyph_info:
                attrib={'xlink:href': '#%s' % glyph_id}
                if xposition != 0.0:
                    attrib['x'] = short_float_fmt(xposition)
                if yposition != 0.0:
                    attrib['y'] = short_float_fmt(yposition)
                writer.element(
                    'use',
                    attrib=attrib)

            writer.end('g')
        else:
            if ismath == "TeX":
                _glyphs = text2path.get_glyphs_tex(prop, s, glyph_map=glyph_map,
                                                   return_new_glyphs_only=True)
            else:
                _glyphs = text2path.get_glyphs_mathtext(prop, s, glyph_map=glyph_map,
                                                        return_new_glyphs_only=True)

            glyph_info, glyph_map_new, rects = _glyphs

            # we store the character glyphs w/o flipping. Instead, the
            # coordinate will be flipped when this characters are
            # used.
            if glyph_map_new:
                writer.start('defs')
                for char_id, glyph_path in glyph_map_new.items():
                    char_id = self._adjust_char_id(char_id)
                    # Some characters are blank
                    if not len(glyph_path[0]):
                        path_data = ""
                    else:
                        path = Path(*glyph_path)
                        path_data = self._convert_path(path, simplify=False)
                    writer.element('path', id=char_id, d=path_data)
                writer.end('defs')

                glyph_map.update(glyph_map_new)

            attrib = {}
            font_scale = fontsize / text2path.FONT_SCALE
            attrib['style'] = generate_css(style)
            attrib['transform'] = generate_transform([
                ('translate', (x, y)),
                ('rotate', (-angle,)),
                ('scale', (font_scale, -font_scale))])

            writer.start('g', attrib=attrib)
            for char_id, xposition, yposition, scale in glyph_info:
                char_id = self._adjust_char_id(char_id)

                writer.element(
                    'use',
                    transform=generate_transform([
                        ('translate', (xposition, yposition)),
                        ('scale', (scale,)),
                        ]),
                    attrib={'xlink:href': '#%s' % char_id})

            for verts, codes in rects:
                path = Path(verts, codes)
                path_data = self._convert_path(path, simplify=False)
                writer.element('path', d=path_data)

            writer.end('g')
