    def get_loc(self, key, method=None):
        self._check_method(method)

        original_key = key
        key = self._maybe_cast_indexed(key)

        if self.is_non_overlapping_monotonic:
            if isinstance(key, Interval):
                left = self._maybe_cast_slice_bound(key.left, 'left', None)
                right = self._maybe_cast_slice_bound(key.right, 'right', None)
                key = Interval(left, right, key.closed)
            else:
                key = self._maybe_cast_slice_bound(key, 'left', None)

            start, stop = self._find_non_overlapping_monotonic_bounds(key)

            if start is None or stop is None:
                return slice(start, stop)
            elif start + 1 == stop:
                return start
            elif start < stop:
                return slice(start, stop)
            else:
                raise KeyError(original_key)

        else:
            # use the interval tree
            if isinstance(key, Interval):
                left, right = _get_interval_closed_bounds(key)
                return self._engine.get_loc_interval(left, right)
            else:
                return self._engine.get_loc(key)
