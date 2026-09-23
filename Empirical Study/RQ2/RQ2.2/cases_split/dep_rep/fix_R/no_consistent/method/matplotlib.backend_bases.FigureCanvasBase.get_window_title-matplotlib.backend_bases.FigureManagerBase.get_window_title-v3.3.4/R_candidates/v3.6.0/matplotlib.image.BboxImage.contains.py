    def contains(self, mouseevent):
        """Test whether the mouse event occurred within the image."""
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info

        if not self.get_visible():  # or self.get_figure()._renderer is None:
            return False, {}

        x, y = mouseevent.x, mouseevent.y
        inside = self.get_window_extent().contains(x, y)

        return inside, {}
