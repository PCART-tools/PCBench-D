    def intersection(self, other):
        """
        Specialized intersection for DatetimeIndex objects. May be much faster
        than Index.intersection

        Parameters
        ----------
        other : DatetimeIndex or array-like

        Returns
        -------
        y : Index or DatetimeIndex
        """
        self._assert_can_do_setop(other)
        if not isinstance(other, DatetimeIndex):
            try:
                other = DatetimeIndex(other)
            except (TypeError, ValueError):
                pass
            result = Index.intersection(self, other)
            if isinstance(result, DatetimeIndex):
                if result.freq is None:
                    result.offset = to_offset(result.inferred_freq)
            return result

        elif (other.offset is None or self.offset is None or
              other.offset != self.offset or
              not other.offset.isAnchored() or
              (not self.is_monotonic or not other.is_monotonic)):
            result = Index.intersection(self, other)
            result = self._shallow_copy(result._values, name=result.name,
                                        tz=result.tz, freq=None)
            if result.freq is None:
                result.offset = to_offset(result.inferred_freq)
            return result

        if len(self) == 0:
            return self
        if len(other) == 0:
            return other
        # to make our life easier, "sort" the two ranges
        if self[0] <= other[0]:
            left, right = self, other
        else:
            left, right = other, self

        end = min(left[-1], right[-1])
        start = right[0]

        if end < start:
            return type(self)(data=[])
        else:
            lslice = slice(*left.slice_locs(start, end))
            left_chunk = left.values[lslice]
            return self._shallow_copy(left_chunk)
