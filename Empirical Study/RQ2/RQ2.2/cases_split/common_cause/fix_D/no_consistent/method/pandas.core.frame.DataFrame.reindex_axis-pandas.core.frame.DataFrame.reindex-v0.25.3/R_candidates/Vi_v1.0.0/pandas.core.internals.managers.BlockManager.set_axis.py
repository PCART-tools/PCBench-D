    def set_axis(self, axis, new_labels):
        new_labels = ensure_index(new_labels)
        old_len = len(self.axes[axis])
        new_len = len(new_labels)

        if new_len != old_len:
            raise ValueError(
                f"Length mismatch: Expected axis has {old_len} elements, new "
                f"values have {new_len} elements"
            )

        self.axes[axis] = new_labels
