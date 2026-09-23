    def _convert_list_indexer(self, keyarr, kind=None):
        """
        we are passed a list indexer.
        Return our indexer or raise if all of the values are not included in the categories
        """
        codes = self.categories.get_indexer(keyarr)
        if (codes==-1).any():
            raise KeyError("a list-indexer must only include values that are in the categories")

        return None
