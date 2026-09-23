    def render_glyph(self, ox, oy, info):
        oy = oy - info.offset - self.height
        thetext = unichr_safe(info.num)
        self.glyphs.append(
            (info.font, info.fontsize, thetext, ox, oy))
