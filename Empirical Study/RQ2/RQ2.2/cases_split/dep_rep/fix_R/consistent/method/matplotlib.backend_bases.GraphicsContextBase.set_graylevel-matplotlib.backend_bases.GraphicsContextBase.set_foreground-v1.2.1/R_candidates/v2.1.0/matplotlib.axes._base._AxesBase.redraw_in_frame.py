    def redraw_in_frame(self):
        """
        This method can only be used after an initial draw which
        caches the renderer.  It is used to efficiently update Axes
        data (axis ticks, labels, etc are not updated)
        """
        if self._cachedRenderer is None:
            msg = ('redraw_in_frame can only be used after an initial draw'
                   ' which caches the render')
            raise AttributeError(msg)
        self.draw(self._cachedRenderer, inframe=True)
