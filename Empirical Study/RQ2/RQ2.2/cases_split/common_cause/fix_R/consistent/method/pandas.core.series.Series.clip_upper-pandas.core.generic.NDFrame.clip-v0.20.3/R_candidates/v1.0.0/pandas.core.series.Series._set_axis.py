    def _set_axis(self, axis, labels, fastpath=False):
        """
        Override generic, we want to set the _typ here.
        """

        if not fastpath:
            labels = ensure_index(labels)

        is_all_dates = labels.is_all_dates
        if is_all_dates:
            if not isinstance(labels, (DatetimeIndex, PeriodIndex, TimedeltaIndex)):
                try:
                    labels = DatetimeIndex(labels)
                    # need to set here because we changed the index
                    if fastpath:
                        self._data.set_axis(axis, labels)
                except (tslibs.OutOfBoundsDatetime, ValueError):
                    # labels may exceeds datetime bounds,
                    # or not be a DatetimeIndex
                    pass

        self._set_subtyp(is_all_dates)

        object.__setattr__(self, "_index", labels)
        if not fastpath:
            self._data.set_axis(axis, labels)
