    def astype(self, dtype, copy: bool = True):
        # We handle
        #   --> datetime
        #   --> period
        # DatetimeLikeArrayMixin Super handles the rest.
        dtype = pandas_dtype(dtype)

        if dtype == self.dtype:
            if copy:
                return self.copy()
            return self

        elif isinstance(dtype, ExtensionDtype):
            if not isinstance(dtype, DatetimeTZDtype):
                # e.g. Sparse[datetime64[ns]]
                return super().astype(dtype, copy=copy)
            elif self.tz is None:
                # pre-2.0 this did self.tz_localize(dtype.tz), which did not match
                #  the Series behavior which did
                #  values.tz_localize("UTC").tz_convert(dtype.tz)
                raise TypeError(
                    "Cannot use .astype to convert from timezone-naive dtype to "
                    "timezone-aware dtype. Use obj.tz_localize instead or "
                    "series.dt.tz_localize instead"
                )
            else:
                # tzaware unit conversion e.g. datetime64[s, UTC]
                np_dtype = np.dtype(dtype.str)
                res_values = astype_overflowsafe(self._ndarray, np_dtype, copy=copy)
                return type(self)._simple_new(res_values, dtype=dtype, freq=self.freq)

        elif (
            self.tz is None
            and lib.is_np_dtype(dtype, "M")
            and not is_unitless(dtype)
            and is_supported_unit(get_unit_from_dtype(dtype))
        ):
            # unit conversion e.g. datetime64[s]
            res_values = astype_overflowsafe(self._ndarray, dtype, copy=True)
            return type(self)._simple_new(res_values, dtype=res_values.dtype)
            # TODO: preserve freq?

        elif self.tz is not None and lib.is_np_dtype(dtype, "M"):
            # pre-2.0 behavior for DTA/DTI was
            #  values.tz_convert("UTC").tz_localize(None), which did not match
            #  the Series behavior
            raise TypeError(
                "Cannot use .astype to convert from timezone-aware dtype to "
                "timezone-naive dtype. Use obj.tz_localize(None) or "
                "obj.tz_convert('UTC').tz_localize(None) instead."
            )

        elif (
            self.tz is None
            and lib.is_np_dtype(dtype, "M")
            and dtype != self.dtype
            and is_unitless(dtype)
        ):
            raise TypeError(
                "Casting to unit-less dtype 'datetime64' is not supported. "
                "Pass e.g. 'datetime64[ns]' instead."
            )

        elif isinstance(dtype, PeriodDtype):
            return self.to_period(freq=dtype.freq)
        return dtl.DatetimeLikeArrayMixin.astype(self, dtype, copy)
