    def draw_artist(self, a):
        """
        draw :class:`matplotlib.artist.Artist` instance *a* only --
        this is available only after the figure is drawn
        """
        if self._cachedRenderer is None:
            msg = ('draw_artist can only be used after an initial draw which'
                   ' caches the render')
            raise AttributeError(msg)
        a.draw(self._cachedRenderer)
