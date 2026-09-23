    def _write_svgfonts(self):
        if not rcParams['svg.fonttype'] == 'svgfont':
            return

        writer = self.writer
        writer.start('defs')
        for font_fname, chars in self._fonts.items():
            font = get_font(font_fname)
            font.set_size(72, 72)
            sfnt = font.get_sfnt()
            writer.start('font', id=sfnt[1, 0, 0, 4].decode("mac_roman"))
            writer.element(
                'font-face',
                attrib={
                    'font-family': font.family_name,
                    'font-style': font.style_name.lower(),
                    'units-per-em': '72',
                    'bbox': ' '.join(
                        short_float_fmt(x / 64.0) for x in font.bbox)})
            for char in chars:
                glyph = font.load_char(char, flags=LOAD_NO_HINTING)
                verts, codes = font.get_path()
                path = Path(verts, codes)
                path_data = self._convert_path(path)
                # name = font.get_glyph_name(char)
                writer.element(
                    'glyph',
                    d=path_data,
                    attrib={
                        # 'glyph-name': name,
                        'unicode': chr(char),
                        'horiz-adv-x':
                        short_float_fmt(glyph.linearHoriAdvance / 65536.0)})
            writer.end('font')
        writer.end('defs')
