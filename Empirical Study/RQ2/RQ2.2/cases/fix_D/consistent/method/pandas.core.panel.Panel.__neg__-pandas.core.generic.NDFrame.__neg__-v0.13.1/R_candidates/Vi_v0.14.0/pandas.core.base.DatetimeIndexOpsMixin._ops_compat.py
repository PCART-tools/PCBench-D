    def _ops_compat(self, name, op_accessor):

        from pandas.tseries.index import DatetimeIndex
        from pandas.tseries.period import PeriodIndex
        obj = self._get_access_object()
        if isinstance(obj, DatetimeIndex):
            self._is_allowed_datetime_index_op(name)
        elif isinstance(obj, PeriodIndex):
            self._is_allowed_period_index_op(name)
        try:
            return self._wrap_access_object(getattr(obj,op_accessor))
        except AttributeError:
            raise TypeError("cannot perform an {name} operations on this type {typ}".format(
                name=name,typ=type(obj)))
