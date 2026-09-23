    def set_axis(self, axis, new_labels):
        new_labels = ensure_index(new_labels)
        old_len = len(self.axes[axis])
        new_len = len(new_labels)

        if new_len != old_len:
            raise ValueError(
                'Length mismatch: Expected axis has {old} elements, new '
                'values have {new} elements'.format(old=old_len, new=new_len))

        self.axes[axis] = new_labels
