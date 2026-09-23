    def render_glyph(self, ox, oy, info):
        oy = self.height - oy + info.offset

        self.svg_glyphs.append(
            (info.font, info.fontsize, info.num, ox, oy, info.metrics))
