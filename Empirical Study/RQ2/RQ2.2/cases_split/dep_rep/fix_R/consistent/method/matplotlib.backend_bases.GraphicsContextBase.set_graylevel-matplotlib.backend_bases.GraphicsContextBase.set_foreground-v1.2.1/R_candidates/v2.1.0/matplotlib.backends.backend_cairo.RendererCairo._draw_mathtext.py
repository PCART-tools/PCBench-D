    def _draw_mathtext(self, gc, x, y, s, prop, angle):
        ctx = gc.ctx
        width, height, descent, glyphs, rects = self.mathtext_parser.parse(
            s, self.dpi, prop)

        ctx.save()
        ctx.translate(x, y)
        if angle:
            ctx.rotate(np.deg2rad(-angle))

        for font, fontsize, s, ox, oy in glyphs:
            ctx.new_path()
            ctx.move_to(ox, oy)

            fontProp = ttfFontProperty(font)
            ctx.save()
            ctx.select_font_face(fontProp.name,
                                 self.fontangles[fontProp.style],
                                 self.fontweights[fontProp.weight])

            size = fontsize * self.dpi / 72.0
            ctx.set_font_size(size)
            if not six.PY3 and isinstance(s, six.text_type):
                s = s.encode("utf-8")
            ctx.show_text(s)
            ctx.restore()

        for ox, oy, w, h in rects:
            ctx.new_path()
            ctx.rectangle(ox, oy, w, h)
            ctx.set_source_rgb(0, 0, 0)
            ctx.fill_preserve()

        ctx.restore()
