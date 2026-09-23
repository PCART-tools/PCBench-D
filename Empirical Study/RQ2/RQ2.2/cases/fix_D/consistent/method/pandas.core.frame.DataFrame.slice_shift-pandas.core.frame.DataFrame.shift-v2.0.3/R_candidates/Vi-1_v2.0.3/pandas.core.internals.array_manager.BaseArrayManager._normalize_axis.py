    @staticmethod
    def _normalize_axis(axis: AxisInt) -> int:
        # switch axis
        axis = 1 if axis == 0 else 0
        return axis
