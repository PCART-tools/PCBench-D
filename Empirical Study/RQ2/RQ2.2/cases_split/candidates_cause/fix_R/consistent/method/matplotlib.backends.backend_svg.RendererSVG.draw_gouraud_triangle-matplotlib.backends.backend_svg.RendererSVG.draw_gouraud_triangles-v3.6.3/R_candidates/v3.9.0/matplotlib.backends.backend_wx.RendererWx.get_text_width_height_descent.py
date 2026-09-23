    def get_text_width_height_descent(self, s, prop, ismath):
        # docstring inherited

        if ismath:
            s = cbook.strip_math(s)

        if self.gc is None:
            gc = self.new_gc()
        else:
            gc = self.gc
        gfx_ctx = gc.gfx_ctx
        font = self.get_wx_font(s, prop)
        gfx_ctx.SetFont(font, wx.BLACK)
        w, h, descent, leading = gfx_ctx.GetFullTextExtent(s)

        return w, h, descent
