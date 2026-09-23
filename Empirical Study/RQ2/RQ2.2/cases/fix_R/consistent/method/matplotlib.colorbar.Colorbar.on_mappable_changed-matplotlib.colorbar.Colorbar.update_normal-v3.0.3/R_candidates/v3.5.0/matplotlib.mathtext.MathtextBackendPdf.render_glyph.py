    def render_glyph(self, ox, oy, info):
        filename = info.font.fname
        oy = self.height - oy + info.offset
        self.glyphs.append(
            (ox, oy, filename, info.fontsize,
             info.num, info.symbol_name))
