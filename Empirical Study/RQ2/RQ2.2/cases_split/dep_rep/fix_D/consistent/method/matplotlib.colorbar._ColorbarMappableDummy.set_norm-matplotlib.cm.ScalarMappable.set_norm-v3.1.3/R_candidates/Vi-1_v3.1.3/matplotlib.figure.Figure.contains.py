    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred on the figure.

        Returns
        -------
            bool, {}
        """
        if self._contains is not None:
            return self._contains(self, mouseevent)
        inside = self.bbox.contains(mouseevent.x, mouseevent.y)
        return inside, {}
