    def _get_resampler_for_grouping(self, groupby: GroupBy, key):
        """
        Return the correct class for resampling with groupby.
        """
        return self._resampler_for_grouping(groupby=groupby, key=key, parent=self)
