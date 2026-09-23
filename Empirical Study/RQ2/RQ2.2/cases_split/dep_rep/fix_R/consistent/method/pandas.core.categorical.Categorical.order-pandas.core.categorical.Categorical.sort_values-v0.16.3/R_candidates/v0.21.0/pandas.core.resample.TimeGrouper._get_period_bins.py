    def _get_period_bins(self, ax):
        if not isinstance(ax, PeriodIndex):
            raise TypeError('axis must be a PeriodIndex, but got '
                            'an instance of %r' % type(ax).__name__)

        memb = ax.asfreq(self.freq, how=self.convention)

        # NaT handling as in pandas._lib.lib.generate_bins_dt64()
        nat_count = 0
        if memb.hasnans:
            nat_count = np.sum(memb._isnan)
            memb = memb[~memb._isnan]

        # if index contains no valid (non-NaT) values, return empty index
        if not len(memb):
            binner = labels = PeriodIndex(
                data=[], freq=self.freq, name=ax.name)
            return binner, [], labels

        start = ax.min().asfreq(self.freq, how=self.convention)
        end = ax.max().asfreq(self.freq, how='end')

        labels = binner = PeriodIndex(start=start, end=end,
                                      freq=self.freq, name=ax.name)

        i8 = memb.asi8
        freq_mult = self.freq.n

        # when upsampling to subperiods, we need to generate enough bins
        expected_bins_count = len(binner) * freq_mult
        i8_extend = expected_bins_count - (i8[-1] - i8[0])
        rng = np.arange(i8[0], i8[-1] + i8_extend, freq_mult)
        rng += freq_mult
        bins = memb.searchsorted(rng, side='left')

        if nat_count > 0:
            # NaT handling as in pandas._lib.lib.generate_bins_dt64()
            # shift bins by the number of NaT
            bins += nat_count
            bins = np.insert(bins, 0, nat_count)
            binner = binner.insert(0, tslib.NaT)
            labels = labels.insert(0, tslib.NaT)

        return binner, bins, labels
