    def draw_artist(self, a):
        """
        Draw `.Artist` instance *a* only.

        This can only be called after the figure has been drawn.
        """
        if self._cachedRenderer is None:
            raise AttributeError("draw_artist can only be used after an "
                                 "initial draw which caches the renderer")
        a.draw(self._cachedRenderer)
