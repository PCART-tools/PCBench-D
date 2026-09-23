    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred on the figure.

        Returns
        -------
            bool, {}
        """
        if self._different_canvas(mouseevent):
            return False, {}
        inside = self.bbox.contains(mouseevent.x, mouseevent.y)
        return inside, {}
