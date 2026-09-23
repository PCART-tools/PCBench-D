    def astype(self, dtype, copy=True):
        # We handle
        #   --> timedelta64[ns]
        #   --> timedelta64
        # DatetimeLikeArrayMixin super call handles other cases
        dtype = pandas_dtype(dtype)

        if is_timedelta64_dtype(dtype) and not is_timedelta64_ns_dtype(dtype):
            # by pandas convention, converting to non-nano timedelta64
            #  returns an int64-dtyped array with ints representing multiples
            #  of the desired timedelta unit.  This is essentially division
            if self._hasnans:
                # avoid double-copying
                result = self._data.astype(dtype, copy=False)
                values = self._maybe_mask_results(result,
                                                  fill_value=None,
                                                  convert='float64')
                return values
            result = self._data.astype(dtype, copy=copy)
            return result.astype('i8')
        elif is_timedelta64_ns_dtype(dtype):
            if copy:
                return self.copy()
            return self
        return dtl.DatetimeLikeArrayMixin.astype(self, dtype, copy=copy)
