    def _set_axis(self, axis, labels, fastpath=False):
        """ override generic, we want to set the _typ here """

        if not fastpath:
            labels = _ensure_index(labels)

        is_all_dates = labels.is_all_dates
        if is_all_dates:
            from pandas.tseries.index import DatetimeIndex
            from pandas.tseries.period import PeriodIndex
            if not isinstance(labels, (DatetimeIndex, PeriodIndex)):
                labels = DatetimeIndex(labels)

                # need to set here becuase we changed the index
                if fastpath:
                    self._data.set_axis(axis, labels)
        self._set_subtyp(is_all_dates)

        object.__setattr__(self, '_index', labels)
        if not fastpath:
            self._data.set_axis(axis, labels)
