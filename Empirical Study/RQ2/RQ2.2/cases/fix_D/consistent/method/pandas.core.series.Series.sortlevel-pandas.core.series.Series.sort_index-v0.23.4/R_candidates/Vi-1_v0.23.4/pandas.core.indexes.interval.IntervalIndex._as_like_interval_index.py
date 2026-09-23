    def _as_like_interval_index(self, other):
        self._assert_can_do_setop(other)
        other = _ensure_index(other)
        if not isinstance(other, IntervalIndex):
            msg = ('the other index needs to be an IntervalIndex too, but '
                   'was type {}').format(other.__class__.__name__)
            raise TypeError(msg)
        elif self.closed != other.closed:
            msg = ('can only do set operations between two IntervalIndex '
                   'objects that are closed on the same side')
            raise ValueError(msg)
        return other
