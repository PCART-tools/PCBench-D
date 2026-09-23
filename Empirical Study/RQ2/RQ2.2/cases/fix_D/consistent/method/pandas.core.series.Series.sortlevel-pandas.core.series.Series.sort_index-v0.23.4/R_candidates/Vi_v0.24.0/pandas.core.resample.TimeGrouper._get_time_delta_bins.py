    def _get_time_delta_bins(self, ax):
        if not isinstance(ax, TimedeltaIndex):
            raise TypeError('axis must be a TimedeltaIndex, but got '
                            'an instance of %r' % type(ax).__name__)

        if not len(ax):
            binner = labels = TimedeltaIndex(
                data=[], freq=self.freq, name=ax.name)
            return binner, [], labels

        start, end = ax.min(), ax.max()
        labels = binner = timedelta_range(start=start,
                                          end=end,
                                          freq=self.freq,
                                          name=ax.name)

        end_stamps = labels + self.freq
        bins = ax.searchsorted(end_stamps, side='left')

        # Addresses GH #10530
        if self.base > 0:
            labels += type(self.freq)(self.base)

        return binner, bins, labels
