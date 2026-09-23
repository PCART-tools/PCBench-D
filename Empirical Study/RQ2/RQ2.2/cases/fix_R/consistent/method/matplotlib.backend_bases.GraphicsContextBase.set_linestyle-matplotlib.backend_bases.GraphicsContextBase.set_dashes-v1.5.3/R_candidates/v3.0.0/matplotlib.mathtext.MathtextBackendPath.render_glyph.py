    def render_glyph(self, ox, oy, info):
        oy = self.height - oy + info.offset
        thetext = info.num
        self.glyphs.append(
            (info.font, info.fontsize, thetext, ox, oy))
