    def draw(self, renderer, *args, **kwargs):
        """
        Draw the Artist using the given renderer.

        This method will be overridden in the Artist subclasses. Typically,
        it is implemented to not have any effect if the Artist is not visible
        (`.Artist.get_visible` is *False*).

        Parameters
        ----------
        renderer : `.RendererBase` subclass.
        """
        if not self.get_visible():
            return
        self.stale = False
