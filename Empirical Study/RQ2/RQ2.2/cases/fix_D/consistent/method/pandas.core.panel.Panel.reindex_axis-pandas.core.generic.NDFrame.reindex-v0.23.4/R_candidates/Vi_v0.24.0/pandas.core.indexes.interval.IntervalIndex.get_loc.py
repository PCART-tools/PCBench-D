    def get_loc(self, key, method=None):
        """Get integer location, slice or boolean mask for requested label.

        Parameters
        ----------
        key : label
        method : {None}, optional
            * default: matches where the label is within an interval only.

        Returns
        -------
        loc : int if unique index, slice if monotonic index, else mask

        Examples
        ---------
        >>> i1, i2 = pd.Interval(0, 1), pd.Interval(1, 2)
        >>> index = pd.IntervalIndex([i1, i2])
        >>> index.get_loc(1)
        0

        You can also supply an interval or an location for a point inside an
        interval.

        >>> index.get_loc(pd.Interval(0, 2))
        array([0, 1], dtype=int64)
        >>> index.get_loc(1.5)
        1

        If a label is in several intervals, you get the locations of all the
        relevant intervals.

        >>> i3 = pd.Interval(0, 2)
        >>> overlapping_index = pd.IntervalIndex([i2, i3])
        >>> overlapping_index.get_loc(1.5)
        array([0, 1], dtype=int64)
        """
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
            key = self._maybe_convert_i8(key)
            if isinstance(key, Interval):
                left, right = _get_interval_closed_bounds(key)
                return self._engine.get_loc_interval(left, right)
            else:
                return self._engine.get_loc(key)
