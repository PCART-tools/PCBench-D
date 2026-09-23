    @doc(Index.astype)
    def astype(self, dtype, copy: bool = True):
        dtype = pandas_dtype(dtype)
        if is_timedelta64_dtype(dtype) and not is_timedelta64_ns_dtype(dtype):
            # Have to repeat the check for 'timedelta64' (not ns) dtype
            #  so that we can return a numeric index, since pandas will return
            #  a TimedeltaIndex when dtype='timedelta'
            result = self._data.astype(dtype, copy=copy)
            if self.hasnans:
                return Index(result, name=self.name)
            return Index(result.astype("i8"), name=self.name)
        return DatetimeIndexOpsMixin.astype(self, dtype, copy=copy)
