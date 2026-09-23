    def _convert_for_datetime(self, lvalues, rvalues):
        mask = None
        # datetimes require views
        if self.is_datetime_lhs or self.is_datetime_rhs:
            # datetime subtraction means timedelta
            if self.is_datetime_lhs and self.is_datetime_rhs:
                self.dtype = 'timedelta64[ns]'
            else:
                self.dtype = 'datetime64[ns]'
            mask = isnull(lvalues) | isnull(rvalues)
            lvalues = lvalues.view(np.int64)
            rvalues = rvalues.view(np.int64)

        # otherwise it's a timedelta
        else:
            self.dtype = 'timedelta64[ns]'
            mask = isnull(lvalues) | isnull(rvalues)
            lvalues = lvalues.astype(np.int64)
            rvalues = rvalues.astype(np.int64)

            # time delta division -> unit less
            # integer gets converted to timedelta in np < 1.6
            if (self.is_timedelta_lhs and self.is_timedelta_rhs) and\
               not self.is_integer_rhs and\
               not self.is_integer_lhs and\
               self.name in ('__div__', '__truediv__'):
                self.dtype = 'float64'
                self.fill_value = np.nan
                lvalues = lvalues.astype(np.float64)
                rvalues = rvalues.astype(np.float64)

        # if we need to mask the results
        if mask is not None:
            if mask.any():
                def f(x):
                    x = np.array(x, dtype=self.dtype)
                    np.putmask(x, mask, self.fill_value)
                    return x
                self.wrap_results = f
        self.lvalues = lvalues
        self.rvalues = rvalues
