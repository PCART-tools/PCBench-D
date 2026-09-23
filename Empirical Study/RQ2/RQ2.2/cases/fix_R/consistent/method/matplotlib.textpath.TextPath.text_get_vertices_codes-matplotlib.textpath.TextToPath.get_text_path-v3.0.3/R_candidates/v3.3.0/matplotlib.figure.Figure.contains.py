    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred on the figure.

        Returns
        -------
            bool, {}
        """
        inside, info = self._default_contains(mouseevent, figure=self)
        if inside is not None:
            return inside, info
        inside = self.bbox.contains(mouseevent.x, mouseevent.y)
        return inside, {}
