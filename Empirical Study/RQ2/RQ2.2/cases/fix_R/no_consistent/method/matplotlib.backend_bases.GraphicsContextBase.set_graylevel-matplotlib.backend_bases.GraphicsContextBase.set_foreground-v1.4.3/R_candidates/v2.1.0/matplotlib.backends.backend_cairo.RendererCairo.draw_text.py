    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # Note: x,y are device/display coords, not user-coords, unlike other
        # draw_* methods
        if ismath:
            self._draw_mathtext(gc, x, y, s, prop, angle)

        else:
            ctx = gc.ctx
            ctx.new_path()
            ctx.move_to(x, y)
            ctx.select_font_face(prop.get_name(),
                                 self.fontangles[prop.get_style()],
                                 self.fontweights[prop.get_weight()])

            size = prop.get_size_in_points() * self.dpi / 72.0

            ctx.save()
            if angle:
                ctx.rotate(np.deg2rad(-angle))
            ctx.set_font_size(size)

            if HAS_CAIRO_CFFI:
                if not isinstance(s, six.text_type):
                    s = six.text_type(s)
            else:
                if not six.PY3 and isinstance(s, six.text_type):
                    s = s.encode("utf-8")

            ctx.show_text(s)
            ctx.restore()
