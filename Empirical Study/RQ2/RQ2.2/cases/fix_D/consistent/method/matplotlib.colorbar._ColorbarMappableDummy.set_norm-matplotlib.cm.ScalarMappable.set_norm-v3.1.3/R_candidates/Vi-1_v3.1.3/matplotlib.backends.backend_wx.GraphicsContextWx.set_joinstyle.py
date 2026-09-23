    def set_joinstyle(self, js):
        # docstring inherited
        DEBUG_MSG("set_joinstyle()", 1, self)
        self.select()
        GraphicsContextBase.set_joinstyle(self, js)
        self._pen.SetJoin(GraphicsContextWx._joind[self._joinstyle])
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()
