    def set_linewidth(self, w):
        # docstring inherited
        w = float(w)
        DEBUG_MSG("set_linewidth()", 1, self)
        self.select()
        if 0 < w < 1:
            w = 1
        GraphicsContextBase.set_linewidth(self, w)
        lw = int(self.renderer.points_to_pixels(self._linewidth))
        if lw == 0:
            lw = 1
        self._pen.SetWidth(lw)
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()
