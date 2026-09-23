    def _setop(op_name):
        def func(self, other):
            msg = ('can only do set operations between two IntervalIndex '
                   'objects that are closed on the same side')
            other = self._as_like_interval_index(other, msg)
            result = getattr(self._multiindex, op_name)(other._multiindex)
            result_name = self.name if self.name == other.name else None
            return type(self).from_tuples(result.values, closed=self.closed,
                                          name=result_name)
        return func
