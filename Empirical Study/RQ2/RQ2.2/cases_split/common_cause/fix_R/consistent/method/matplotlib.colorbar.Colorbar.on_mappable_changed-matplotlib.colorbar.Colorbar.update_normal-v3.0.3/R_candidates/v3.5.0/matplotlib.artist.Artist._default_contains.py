    def _default_contains(self, mouseevent, figure=None):
        """
        Base impl. for checking whether a mouseevent happened in an artist.

        1. If the artist figure is known and the event did not occur in that
           figure (by checking its ``canvas`` attribute), reject it.
        2. Otherwise, return `None, {}`, indicating that the subclass'
           implementation should be used.

        Subclasses should start their definition of `contains` as follows:

            inside, info = self._default_contains(mouseevent)
            if inside is not None:
                return inside, info
            # subclass-specific implementation follows

        The *figure* kwarg is provided for the implementation of
        `.Figure.contains`.
        """
        if figure is not None and mouseevent.canvas is not figure.canvas:
            return False, {}
        return None, {}
