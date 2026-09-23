    def draw_artist(self, a):
        """
        Draw `.Artist` *a* only.

        This method can only be used after an initial draw of the figure,
        because that creates and caches the renderer needed here.
        """
        if self._cachedRenderer is None:
            raise AttributeError("draw_artist can only be used after an "
                                 "initial draw which caches the renderer")
        a.draw(self._cachedRenderer)
