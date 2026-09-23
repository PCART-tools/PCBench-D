    @_api.delete_parameter("3.3", "args")
    @_api.delete_parameter("3.3", "kwargs")
    def draw(self, renderer, *args, **kwargs):
        """
        Draw the Artist (and its children) using the given renderer.

        This has no effect if the artist is not visible (`.Artist.get_visible`
        returns False).

        Parameters
        ----------
        renderer : `.RendererBase` subclass.

        Notes
        -----
        This method is overridden in the Artist subclasses.
        """
        if not self.get_visible():
            return
        self.stale = False
