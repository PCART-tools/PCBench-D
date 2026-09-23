    def set_capstyle(self, cs):
        # docstring inherited
        _log.debug("%s - set_capstyle()", type(self))
        self.select()
        super().set_capstyle(cs)
        self._pen.SetCap(GraphicsContextWx._capd[self._capstyle])
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()
