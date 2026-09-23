    def draw_artist(self, a):
        """
        Draw :class:`matplotlib.artist.Artist` instance *a* only.
        This is available only after the figure is drawn.
        """
        if self._cachedRenderer is None:
            raise AttributeError("draw_artist can only be used after an "
                                 "initial draw which caches the renderer")
        a.draw(self._cachedRenderer)
