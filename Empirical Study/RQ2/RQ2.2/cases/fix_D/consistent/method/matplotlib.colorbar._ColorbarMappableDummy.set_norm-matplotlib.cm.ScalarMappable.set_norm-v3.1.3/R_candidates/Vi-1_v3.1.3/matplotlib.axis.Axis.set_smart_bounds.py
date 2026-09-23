    def set_smart_bounds(self, value):
        """Set the axis to have smart bounds."""
        self._smart_bounds = value
        self.stale = True
