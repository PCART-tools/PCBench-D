    def draw_artist(self, a):
        """
        This method can only be used after an initial draw which
        caches the renderer.  It is used to efficiently update Axes
        data (axis ticks, labels, etc are not updated)
        """
        if self._cachedRenderer is None:
            msg = ('draw_artist can only be used after an initial draw which'
                   ' caches the render')
            raise AttributeError(msg)
        a.draw(self._cachedRenderer)
