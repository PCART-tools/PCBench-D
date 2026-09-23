    def set_smart_bounds(self, value):
        """set the axis to have smart bounds"""
        self._smart_bounds = value
        self.stale = True
