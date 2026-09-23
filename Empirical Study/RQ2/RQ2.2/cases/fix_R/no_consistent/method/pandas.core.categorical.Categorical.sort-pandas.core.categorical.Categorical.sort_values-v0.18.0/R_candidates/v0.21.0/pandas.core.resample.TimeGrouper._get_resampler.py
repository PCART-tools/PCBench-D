    def _get_resampler(self, obj, kind=None):
        """
        return my resampler or raise if we have an invalid axis

        Parameters
        ----------
        obj : input object
        kind : string, optional
            'period','timestamp','timedelta' are valid

        Returns
        -------
        a Resampler

        Raises
        ------
        TypeError if incompatible axis

        """
        self._set_grouper(obj)

        ax = self.ax
        if isinstance(ax, DatetimeIndex):
            return DatetimeIndexResampler(obj,
                                          groupby=self,
                                          kind=kind,
                                          axis=self.axis)
        elif isinstance(ax, PeriodIndex) or kind == 'period':
            return PeriodIndexResampler(obj,
                                        groupby=self,
                                        kind=kind,
                                        axis=self.axis)
        elif isinstance(ax, TimedeltaIndex):
            return TimedeltaIndexResampler(obj,
                                           groupby=self,
                                           axis=self.axis)

        raise TypeError("Only valid with DatetimeIndex, "
                        "TimedeltaIndex or PeriodIndex, "
                        "but got an instance of %r" % type(ax).__name__)
