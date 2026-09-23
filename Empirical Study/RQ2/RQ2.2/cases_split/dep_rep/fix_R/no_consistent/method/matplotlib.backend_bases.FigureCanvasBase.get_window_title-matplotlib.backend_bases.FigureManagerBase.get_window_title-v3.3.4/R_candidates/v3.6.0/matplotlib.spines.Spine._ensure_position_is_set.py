    def _ensure_position_is_set(self):
        if self._position is None:
            # default position
            self._position = ('outward', 0.0)  # in points
            self.set_position(self._position)
