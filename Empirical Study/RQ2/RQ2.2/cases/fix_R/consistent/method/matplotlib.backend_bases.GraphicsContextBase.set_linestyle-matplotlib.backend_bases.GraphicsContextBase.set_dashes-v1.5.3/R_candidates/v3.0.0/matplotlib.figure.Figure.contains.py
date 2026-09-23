    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred on the figure.

        Returns
        -------
            bool, {}
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)
        inside = self.bbox.contains(mouseevent.x, mouseevent.y)
        return inside, {}
