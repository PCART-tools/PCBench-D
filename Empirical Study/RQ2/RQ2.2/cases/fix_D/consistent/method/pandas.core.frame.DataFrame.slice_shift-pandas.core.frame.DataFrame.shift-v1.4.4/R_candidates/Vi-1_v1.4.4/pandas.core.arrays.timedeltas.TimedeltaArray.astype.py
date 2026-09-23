    def astype(self, dtype, copy: bool = True):
        # We handle
        #   --> timedelta64[ns]
        #   --> timedelta64
        # DatetimeLikeArrayMixin super call handles other cases
        dtype = pandas_dtype(dtype)

        if dtype.kind == "m":
            return astype_td64_unit_conversion(self._ndarray, dtype, copy=copy)

        return dtl.DatetimeLikeArrayMixin.astype(self, dtype, copy=copy)
