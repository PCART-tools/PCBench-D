    @doc(Index._convert_list_indexer)
    def _convert_list_indexer(self, keyarr):
        # Return our indexer or raise if all of the values are not included in
        # the categories

        if self.categories._defer_to_indexing:
            # See tests.indexing.interval.test_interval:test_loc_getitem_frame
            indexer = self.categories._convert_list_indexer(keyarr)
            return Index(self.codes).get_indexer_for(indexer)

        return self.get_indexer_for(keyarr)
