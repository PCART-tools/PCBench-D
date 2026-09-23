    def _get_period_bins(self, ax: PeriodIndex):
        if not isinstance(ax, PeriodIndex):
            raise TypeError(
                "axis must be a PeriodIndex, but got "
                f"an instance of {type(ax).__name__}"
            )

        memb = ax.asfreq(self.freq, how=self.convention)

        # NaT handling as in pandas._lib.lib.generate_bins_dt64()
        nat_count = 0
        if memb.hasnans:
            nat_count = np.sum(memb._isnan)
            memb = memb[~memb._isnan]

        if not len(memb):
            # index contains no valid (non-NaT) values
            bins = np.array([], dtype=np.int64)
            binner = labels = PeriodIndex(data=[], freq=self.freq, name=ax.name)
            if len(ax) > 0:
                # index is all NaT
                binner, bins, labels = _insert_nat_bin(binner, bins, labels, len(ax))
            return binner, bins, labels

        freq_mult = self.freq.n

        start = ax.min().asfreq(self.freq, how=self.convention)
        end = ax.max().asfreq(self.freq, how="end")
        bin_shift = 0

        if isinstance(self.freq, Tick):
            # GH 23882 & 31809: get adjusted bin edge labels with 'origin'
            # and 'origin' support. This call only makes sense if the freq is a
            # Tick since offset and origin are only used in those cases.
            # Not doing this check could create an extra empty bin.
            p_start, end = _get_period_range_edges(
                start,
                end,
                self.freq,
                closed=self.closed,
                origin=self.origin,
                offset=self.offset,
            )

            # Get offset for bin edge (not label edge) adjustment
            start_offset = Period(start, self.freq) - Period(p_start, self.freq)
            # error: Item "Period" of "Union[Period, Any]" has no attribute "n"
            bin_shift = start_offset.n % freq_mult  # type: ignore[union-attr]
            start = p_start

        labels = binner = period_range(
            start=start, end=end, freq=self.freq, name=ax.name
        )

        i8 = memb.asi8

        # when upsampling to subperiods, we need to generate enough bins
        expected_bins_count = len(binner) * freq_mult
        i8_extend = expected_bins_count - (i8[-1] - i8[0])
        rng = np.arange(i8[0], i8[-1] + i8_extend, freq_mult)
        rng += freq_mult
        # adjust bin edge indexes to account for base
        rng -= bin_shift

        # Wrap in PeriodArray for PeriodArray.searchsorted
        prng = type(memb._data)(rng, dtype=memb.dtype)
        bins = memb.searchsorted(prng, side="left")

        if nat_count > 0:
            binner, bins, labels = _insert_nat_bin(binner, bins, labels, nat_count)

        return binner, bins, labels
