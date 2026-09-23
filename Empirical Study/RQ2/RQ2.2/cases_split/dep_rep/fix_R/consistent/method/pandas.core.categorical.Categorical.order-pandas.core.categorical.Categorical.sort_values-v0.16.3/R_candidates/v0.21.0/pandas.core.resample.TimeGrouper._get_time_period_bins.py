    def _get_time_period_bins(self, ax):
        if not isinstance(ax, DatetimeIndex):
            raise TypeError('axis must be a DatetimeIndex, but got '
                            'an instance of %r' % type(ax).__name__)

        if not len(ax):
            binner = labels = PeriodIndex(
                data=[], freq=self.freq, name=ax.name)
            return binner, [], labels

        labels = binner = PeriodIndex(start=ax[0],
                                      end=ax[-1],
                                      freq=self.freq,
                                      name=ax.name)

        end_stamps = (labels + 1).asfreq(self.freq, 's').to_timestamp()
        if ax.tzinfo:
            end_stamps = end_stamps.tz_localize(ax.tzinfo)
        bins = ax.searchsorted(end_stamps, side='left')

        return binner, bins, labels
