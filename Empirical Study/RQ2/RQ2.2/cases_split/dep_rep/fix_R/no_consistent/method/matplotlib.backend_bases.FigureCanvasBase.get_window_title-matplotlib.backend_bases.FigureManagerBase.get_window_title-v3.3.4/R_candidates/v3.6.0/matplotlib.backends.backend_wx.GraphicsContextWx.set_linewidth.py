    def set_linewidth(self, w):
        # docstring inherited
        w = float(w)
        _log.debug("%s - set_linewidth()", type(self))
        self.select()
        if 0 < w < 1:
            w = 1
        super().set_linewidth(w)
        lw = int(self.renderer.points_to_pixels(self._linewidth))
        if lw == 0:
            lw = 1
        self._pen.SetWidth(lw)
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()
