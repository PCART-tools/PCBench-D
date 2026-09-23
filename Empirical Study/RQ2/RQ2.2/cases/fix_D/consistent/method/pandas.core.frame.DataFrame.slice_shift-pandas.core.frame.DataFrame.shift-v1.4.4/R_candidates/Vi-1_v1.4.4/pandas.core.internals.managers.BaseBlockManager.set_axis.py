    def set_axis(self, axis: int, new_labels: Index) -> None:
        # Caller is responsible for ensuring we have an Index object.
        self._validate_set_axis(axis, new_labels)
        self.axes[axis] = new_labels
