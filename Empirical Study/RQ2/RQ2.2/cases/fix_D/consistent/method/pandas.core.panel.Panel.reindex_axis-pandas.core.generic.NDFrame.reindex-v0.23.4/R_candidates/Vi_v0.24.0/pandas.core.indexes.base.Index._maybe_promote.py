    def _maybe_promote(self, other):
        # A hack, but it works
        from pandas import DatetimeIndex
        if self.inferred_type == 'date' and isinstance(other, DatetimeIndex):
            return DatetimeIndex(self), other
        elif self.inferred_type == 'boolean':
            if not is_object_dtype(self.dtype):
                return self.astype('object'), other.astype('object')
        return self, other
