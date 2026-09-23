    def resample(self, rule, how=None, axis=0, fill_method=None,
                 closed=None, label=None, convention='start',
                 kind=None, loffset=None, limit=None, base=0):
        """
        Convenience method for frequency conversion and resampling of regular
        time-series data.

        Parameters
        ----------
        rule : string
            the offset string or object representing target conversion
        how : string
            method for down- or re-sampling, default to 'mean' for
            downsampling
        axis : int, optional, default 0
        fill_method : string, default None
            fill_method for upsampling
        closed : {'right', 'left'}
            Which side of bin interval is closed
        label : {'right', 'left'}
            Which bin edge label to label bucket with
        convention : {'start', 'end', 's', 'e'}
        kind : "period"/"timestamp"
        loffset : timedelta
            Adjust the resampled time labels
        limit : int, default None
            Maximum size gap to when reindexing with fill_method
        base : int, default 0
            For frequencies that evenly subdivide 1 day, the "origin" of the
            aggregated intervals. For example, for '5min' frequency, base could
            range from 0 through 4. Defaults to 0
        """
        from pandas.tseries.resample import TimeGrouper
        axis = self._get_axis_number(axis)
        sampler = TimeGrouper(rule, label=label, closed=closed, how=how,
                              axis=axis, kind=kind, loffset=loffset,
                              fill_method=fill_method, convention=convention,
                              limit=limit, base=base)
        return sampler.resample(self).__finalize__(self)
