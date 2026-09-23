    def set_axis(self, axis: AxisInt, new_labels: Index) -> None:
        # Caller is responsible for ensuring we have an Index object.
        self._validate_set_axis(axis, new_labels)
        axis = self._normalize_axis(axis)
        self._axes[axis] = new_labels
