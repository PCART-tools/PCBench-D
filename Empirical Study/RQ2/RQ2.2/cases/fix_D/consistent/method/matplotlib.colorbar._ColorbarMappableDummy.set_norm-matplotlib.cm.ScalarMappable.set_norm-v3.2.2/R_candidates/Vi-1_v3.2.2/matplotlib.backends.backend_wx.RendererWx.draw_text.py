    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # docstring inherited

        if ismath:
            s = cbook.strip_math(s)
        DEBUG_MSG("draw_text()", 1, self)
        gc.select()
        self.handle_clip_rectangle(gc)
        gfx_ctx = gc.gfx_ctx

        font = self.get_wx_font(s, prop)
        color = gc.get_wxcolour(gc.get_rgb())
        gfx_ctx.SetFont(font, color)

        w, h, d = self.get_text_width_height_descent(s, prop, ismath)
        x = int(x)
        y = int(y - h)

        if angle == 0.0:
            gfx_ctx.DrawText(s, x, y)
        else:
            rads = math.radians(angle)
            xo = h * math.sin(rads)
            yo = h * math.cos(rads)
            gfx_ctx.DrawRotatedText(s, x - xo, y - yo, rads)

        gc.unselect()
