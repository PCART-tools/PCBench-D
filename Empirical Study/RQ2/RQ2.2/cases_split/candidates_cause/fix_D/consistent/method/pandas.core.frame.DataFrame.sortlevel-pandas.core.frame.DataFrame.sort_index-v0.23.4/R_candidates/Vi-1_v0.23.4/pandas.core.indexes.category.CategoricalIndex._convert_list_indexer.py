    @Appender(_index_shared_docs['_convert_list_indexer'])
    def _convert_list_indexer(self, keyarr, kind=None):
        # Return our indexer or raise if all of the values are not included in
        # the categories

        if self.categories._defer_to_indexing:
            indexer = self.categories._convert_list_indexer(keyarr, kind=kind)
            return Index(self.codes).get_indexer_for(indexer)

        indexer = self.categories.get_indexer(np.asarray(keyarr))
        if (indexer == -1).any():
            raise KeyError(
                "a list-indexer must only "
                "include values that are "
                "in the categories")

        return self.get_indexer(keyarr)
