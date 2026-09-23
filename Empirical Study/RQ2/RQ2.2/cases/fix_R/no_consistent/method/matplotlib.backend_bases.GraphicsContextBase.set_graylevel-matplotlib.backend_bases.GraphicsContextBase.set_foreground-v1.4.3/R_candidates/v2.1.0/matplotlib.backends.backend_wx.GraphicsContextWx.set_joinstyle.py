    def set_joinstyle(self, js):
        """
        Set the join style to be one of ('miter', 'round', 'bevel')
        """
        DEBUG_MSG("set_joinstyle()", 1, self)
        self.select()
        GraphicsContextBase.set_joinstyle(self, js)
        self._pen.SetJoin(GraphicsContextWx._joind[self._joinstyle])
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()
