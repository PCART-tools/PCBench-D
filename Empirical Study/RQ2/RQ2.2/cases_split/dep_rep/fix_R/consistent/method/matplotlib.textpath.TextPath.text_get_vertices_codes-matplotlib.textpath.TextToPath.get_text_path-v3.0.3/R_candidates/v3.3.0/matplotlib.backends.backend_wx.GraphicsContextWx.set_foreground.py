    def set_foreground(self, fg, isRGBA=None):
        # docstring inherited
        # Implementation note: wxPython has a separate concept of pen and
        # brush - the brush fills any outline trace left by the pen.
        # Here we set both to the same colour - if a figure is not to be
        # filled, the renderer will set the brush to be transparent
        # Same goes for text foreground...
        _log.debug("%s - set_foreground()", type(self))
        self.select()
        GraphicsContextBase.set_foreground(self, fg, isRGBA)

        self._pen.SetColour(self.get_wxcolour(self.get_rgb()))
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()
