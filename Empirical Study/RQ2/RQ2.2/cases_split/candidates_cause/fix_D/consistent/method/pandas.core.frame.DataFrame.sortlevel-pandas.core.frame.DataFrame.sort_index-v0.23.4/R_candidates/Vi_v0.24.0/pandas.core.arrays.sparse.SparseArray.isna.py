    def isna(self):
        from pandas import isna
        # If null fill value, we want SparseDtype[bool, true]
        # to preserve the same memory usage.
        dtype = SparseDtype(bool, self._null_fill_value)
        return type(self)._simple_new(isna(self.sp_values),
                                      self.sp_index, dtype)
