    def _get_resampler_for_grouping(self, groupby, key=None):
        """
        Return the correct class for resampling with groupby.
        """
        return self._resampler_for_grouping(self, groupby=groupby, key=key)
