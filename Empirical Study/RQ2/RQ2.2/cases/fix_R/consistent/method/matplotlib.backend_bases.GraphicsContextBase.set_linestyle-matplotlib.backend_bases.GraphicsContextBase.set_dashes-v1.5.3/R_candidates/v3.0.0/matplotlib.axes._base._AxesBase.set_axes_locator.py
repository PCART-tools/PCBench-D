    def set_axes_locator(self, locator):
        """
        Set the axes locator.

        Parameters
        ----------
        locator : Callable[[Axes, Renderer], Bbox]
        """
        self._axes_locator = locator
        self.stale = True
