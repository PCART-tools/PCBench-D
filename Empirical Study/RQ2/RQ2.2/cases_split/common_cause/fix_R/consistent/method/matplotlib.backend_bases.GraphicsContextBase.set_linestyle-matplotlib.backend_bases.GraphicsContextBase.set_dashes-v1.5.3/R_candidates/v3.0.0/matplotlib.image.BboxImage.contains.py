    def contains(self, mouseevent):
        """Test whether the mouse event occurred within the image."""
        if callable(self._contains):
            return self._contains(self, mouseevent)

        if not self.get_visible():  # or self.get_figure()._renderer is None:
            return False, {}

        x, y = mouseevent.x, mouseevent.y
        inside = self.get_window_extent().contains(x, y)

        return inside, {}
