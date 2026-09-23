    def draw(self, renderer):
        """
        Draw the Artist (and its children) using the given renderer.

        This has no effect if the artist is not visible (`.Artist.get_visible`
        returns False).

        Parameters
        ----------
        renderer : `~matplotlib.backend_bases.RendererBase` subclass.

        Notes
        -----
        This method is overridden in the Artist subclasses.
        """
        if not self.get_visible():
            return
        self.stale = False
