    def _get_resampler_for_grouping(self, groupby, **kwargs):
        """
        Return the correct class for resampling with groupby.
        """
        return self._resampler_for_grouping(self, groupby=groupby, **kwargs)
