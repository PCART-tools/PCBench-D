    def _downsample(self, how, **kwargs):
        """
        Downsample the cython defined function.

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

        if is_subperiod(ax.freq, self.freq):
            # Downsampling
            return self._groupby_and_aggregate(how, grouper=self.grouper,
                                               **kwargs)
        elif is_superperiod(ax.freq, self.freq):
            if how == 'ohlc':
                # GH #13083
                # upsampling to subperiods is handled as an asfreq, which works
                # for pure aggregating/reducing methods
                # OHLC reduces along the time dimension, but creates multiple
                # values for each period -> handle by _groupby_and_aggregate()
                return self._groupby_and_aggregate(how, grouper=self.grouper)
            return self.asfreq()
        elif ax.freq == self.freq:
            return self.asfreq()

        raise IncompatibleFrequency(
            'Frequency {} cannot be resampled to {}, as they are not '
            'sub or super periods'.format(ax.freq, self.freq))
