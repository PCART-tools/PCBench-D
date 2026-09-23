    def _find_non_overlapping_monotonic_bounds(self, key):
        if isinstance(key, IntervalMixin):
            start = self._searchsorted_monotonic(
                key.left, 'left', exclude_label=key.open_left)
            stop = self._searchsorted_monotonic(
                key.right, 'right', exclude_label=key.open_right)
        elif isinstance(key, slice):
            # slice
            start, stop = key.start, key.stop
            if (key.step or 1) != 1:
                raise NotImplementedError("cannot slice with a slice step")
            if start is None:
                start = 0
            else:
                start = self._searchsorted_monotonic(start, 'left')
            if stop is None:
                stop = len(self)
            else:
                stop = self._searchsorted_monotonic(stop, 'right')
        else:
            # scalar or index-like

            start = self._searchsorted_monotonic(key, 'left')
            stop = self._searchsorted_monotonic(key, 'right')
        return start, stop
