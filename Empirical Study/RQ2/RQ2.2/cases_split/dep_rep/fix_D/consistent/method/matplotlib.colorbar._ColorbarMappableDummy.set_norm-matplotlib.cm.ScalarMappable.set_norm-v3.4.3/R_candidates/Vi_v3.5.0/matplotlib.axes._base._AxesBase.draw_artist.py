    def draw_artist(self, a):
        """
        Efficiently redraw a single artist.

        This method can only be used after an initial draw of the figure,
        because that creates and caches the renderer needed here.
        """
        if self.figure._cachedRenderer is None:
            raise AttributeError("draw_artist can only be used after an "
                                 "initial draw which caches the renderer")
        a.draw(self.figure._cachedRenderer)
