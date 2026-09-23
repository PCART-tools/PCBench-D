    def _normalize_axis(self, axis: AxisInt) -> int:
        # switch axis to follow BlockManager logic
        if self.ndim == 2:
            axis = 1 if axis == 0 else 0
        return axis
