    def get_slice_bound(self, label, side, kind):

        if not isinstance(label, tuple):
            label = label,
        return self._partial_tup_index(label, side=side)
