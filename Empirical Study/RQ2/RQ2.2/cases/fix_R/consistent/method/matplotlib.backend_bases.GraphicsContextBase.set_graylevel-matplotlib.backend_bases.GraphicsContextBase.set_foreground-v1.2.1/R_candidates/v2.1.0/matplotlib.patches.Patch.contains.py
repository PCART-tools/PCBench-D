    def contains(self, mouseevent, radius=None):
        """Test whether the mouse event occurred in the patch.

        Returns T/F, {}
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)
        radius = self._process_radius(radius)
        inside = self.get_path().contains_point(
            (mouseevent.x, mouseevent.y), self.get_transform(), radius)
        return inside, {}
