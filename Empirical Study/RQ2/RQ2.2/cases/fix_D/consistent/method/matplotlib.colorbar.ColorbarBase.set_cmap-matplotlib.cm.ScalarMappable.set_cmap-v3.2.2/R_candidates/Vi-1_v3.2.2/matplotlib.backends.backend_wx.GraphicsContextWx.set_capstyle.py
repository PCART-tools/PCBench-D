    def set_capstyle(self, cs):
        # docstring inherited
        DEBUG_MSG("set_capstyle()", 1, self)
        self.select()
        GraphicsContextBase.set_capstyle(self, cs)
        self._pen.SetCap(GraphicsContextWx._capd[self._capstyle])
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()
