    def set_foreground(self, fg, isRGBA=None):
        """
        Set the foreground color.  fg can be a matlab format string, a
        html hex color string, an rgb unit tuple, or a float between 0
        and 1.  In the latter case, grayscale is used.
        """
        # Implementation note: wxPython has a separate concept of pen and
        # brush - the brush fills any outline trace left by the pen.
        # Here we set both to the same colour - if a figure is not to be
        # filled, the renderer will set the brush to be transparent
        # Same goes for text foreground...
        DEBUG_MSG("set_foreground()", 1, self)
        self.select()
        GraphicsContextBase.set_foreground(self, fg, isRGBA)

        self._pen.SetColour(self.get_wxcolour(self.get_rgb()))
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()
