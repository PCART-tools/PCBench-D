    def get_text_width_height_descent(self, s, prop, ismath):
        # docstring inherited

        if ismath:
            width, height, descent, fonts, used_characters = \
                self.mathtext_parser.parse(s, self.dpi, prop)
            return width, height, descent

        ctx = self.text_ctx
        ctx.save()
        ctx.select_font_face(prop.get_name(),
                             self.fontangles[prop.get_style()],
                             self.fontweights[prop.get_weight()])

        # Cairo (says it) uses 1/96 inch user space units, ref: cairo_gstate.c
        # but if /96.0 is used the font is too small
        size = prop.get_size_in_points() * self.dpi / 72

        # problem - scale remembers last setting and font can become
        # enormous causing program to crash
        # save/restore prevents the problem
        ctx.set_font_size(size)

        y_bearing, w, h = ctx.text_extents(s)[1:4]
        ctx.restore()

        return w, h, h + y_bearing
