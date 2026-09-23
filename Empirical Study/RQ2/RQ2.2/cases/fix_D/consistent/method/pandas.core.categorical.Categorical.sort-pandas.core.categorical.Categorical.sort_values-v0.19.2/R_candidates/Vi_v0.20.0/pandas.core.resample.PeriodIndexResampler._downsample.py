    def _downsample(self, how, **kwargs):
        """
        Downsample the cython defined function

        Parameters
        ----------
        how : string / cython mapped function
        **kwargs : kw args passed to how function
        """

        # we may need to actually resample as if we are timestamps
        if self.kind == 'timestamp':
            return super(PeriodIndexResampler, self)._downsample(how, **kwargs)

        how = self._is_cython_func(how) or how
        ax = self.ax

        new_index = self._get_new_index()

        # Start vs. end of period
        memb = ax.asfreq(self.freq, how=self.convention)

        if is_subperiod(ax.freq, self.freq):
            # Downsampling
            if len(new_index) == 0:
                bins = []
            else:
                i8 = memb.asi8
                rng = np.arange(i8[0], i8[-1] + 1)
                bins = memb.searchsorted(rng, side='right')
            grouper = BinGrouper(bins, new_index)
            return self._groupby_and_aggregate(how, grouper=grouper)
        elif is_superperiod(ax.freq, self.freq):
            return self.asfreq()
        elif ax.freq == self.freq:
            return self.asfreq()

        raise IncompatibleFrequency(
            'Frequency {} cannot be resampled to {}, as they are not '
            'sub or super periods'.format(ax.freq, self.freq))
