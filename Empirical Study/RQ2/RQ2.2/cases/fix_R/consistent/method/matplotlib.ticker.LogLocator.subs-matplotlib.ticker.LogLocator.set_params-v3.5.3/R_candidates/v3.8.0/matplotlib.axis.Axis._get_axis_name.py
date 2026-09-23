    def _get_axis_name(self):
        """Return the axis name."""
        return [name for name, axis in self.axes._axis_map.items()
                if axis is self][0]
