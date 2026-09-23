    def _get_binner(self):
        """
        Create the BinGrouper, assume that self.set_grouper(obj)
        has already been called.
        """

        binner, bins, binlabels = self._get_binner_for_time()
        bin_grouper = BinGrouper(bins, binlabels, indexer=self.groupby.indexer)
        return binner, bin_grouper
