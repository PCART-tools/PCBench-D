    def _convert_for_datetime(self, lvalues, rvalues):
        from pandas.tseries.timedeltas import to_timedelta

        mask = isnull(lvalues) | isnull(rvalues)

        # datetimes require views
        if self.is_datetime_lhs or self.is_datetime_rhs:

            # datetime subtraction means timedelta
            if self.is_datetime_lhs and self.is_datetime_rhs:
                if self.name in ('__sub__', '__rsub__'):
                    self.dtype = 'timedelta64[ns]'
                else:
                    self.dtype = 'datetime64[ns]'
            elif self.is_datetime64tz_lhs:
                self.dtype = lvalues.dtype
            elif self.is_datetime64tz_rhs:
                self.dtype = rvalues.dtype
            else:
                self.dtype = 'datetime64[ns]'

            # if adding single offset try vectorized path
            # in DatetimeIndex; otherwise elementwise apply
            def _offset(lvalues, rvalues):
                if len(lvalues) == 1:
                    rvalues = pd.DatetimeIndex(rvalues)
                    lvalues = lvalues[0]
                else:
                    warnings.warn("Adding/subtracting array of DateOffsets to "
                                  "Series not vectorized", PerformanceWarning)
                    rvalues = rvalues.astype('O')

                # pass thru on the na_op
                self.na_op = lambda x, y: getattr(x, self.name)(y)
                return lvalues, rvalues

            if self.is_offset_lhs:
                lvalues, rvalues = _offset(lvalues, rvalues)
            elif self.is_offset_rhs:
                rvalues, lvalues = _offset(rvalues, lvalues)
            else:

                # with tz, convert to UTC
                if self.is_datetime64tz_lhs:
                    lvalues = lvalues.tz_localize(None)
                if self.is_datetime64tz_rhs:
                    rvalues = rvalues.tz_localize(None)

                lvalues = lvalues.view(np.int64)
                rvalues = rvalues.view(np.int64)

        # otherwise it's a timedelta
        else:

            self.dtype = 'timedelta64[ns]'

            # convert Tick DateOffset to underlying delta
            if self.is_offset_lhs:
                lvalues = to_timedelta(lvalues, box=False)
            if self.is_offset_rhs:
                rvalues = to_timedelta(rvalues, box=False)

            lvalues = lvalues.astype(np.int64)
            if not self.is_floating_rhs:
                rvalues = rvalues.astype(np.int64)

            # time delta division -> unit less
            # integer gets converted to timedelta in np < 1.6
            if ((self.is_timedelta_lhs and self.is_timedelta_rhs) and
                    not self.is_integer_rhs and not self.is_integer_lhs and
                    self.name in ('__div__', '__truediv__')):
                self.dtype = 'float64'
                self.fill_value = np.nan
                lvalues = lvalues.astype(np.float64)
                rvalues = rvalues.astype(np.float64)

        # if we need to mask the results
        if mask.any():

            def f(x):

                # datetime64[ns]/timedelta64[ns] masking
                try:
                    x = np.array(x, dtype=self.dtype)
                except TypeError:
                    x = np.array(x, dtype='datetime64[ns]')

                np.putmask(x, mask, self.fill_value)
                return x

            self.wrap_results = f

        return lvalues, rvalues
