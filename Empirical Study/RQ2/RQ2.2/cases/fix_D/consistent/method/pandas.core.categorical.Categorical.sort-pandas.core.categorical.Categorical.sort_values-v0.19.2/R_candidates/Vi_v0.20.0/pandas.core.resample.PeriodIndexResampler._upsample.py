    def _upsample(self, method, limit=None, fill_value=None):
        """
        method : string {'backfill', 'bfill', 'pad', 'ffill'}
            method for upsampling
        limit : int, default None
            Maximum size gap to fill when reindexing
        fill_value : scalar, default None
            Value to use for missing values

        See also
        --------
        .fillna

        """
        if self._from_selection:
            raise ValueError("Upsampling from level= or on= selection"
                             " is not supported, use .set_index(...)"
                             " to explicitly set index to"
                             " datetime-like")
        # we may need to actually resample as if we are timestamps
        if self.kind == 'timestamp':
            return super(PeriodIndexResampler, self)._upsample(
                method, limit=limit, fill_value=fill_value)

        ax = self.ax
        obj = self.obj
        new_index = self._get_new_index()

        # Start vs. end of period
        memb = ax.asfreq(self.freq, how=self.convention)

        # Get the fill indexer
        indexer = memb.get_indexer(new_index, method=method, limit=limit)
        return self._wrap_result(_take_new_index(
            obj, indexer, new_index, axis=self.axis))
