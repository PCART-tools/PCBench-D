    def _multi_take_opportunity(self, tup):
        """
        Check whether there is the possibility to use ``_multi_take``.
        Currently the limit is that all axes being indexed must be indexed with
        list-likes.

        Parameters
        ----------
        tup : tuple
            Tuple of indexers, one per axis

        Returns
        -------
        boolean: Whether the current indexing can be passed through _multi_take
        """
        if not all(is_list_like_indexer(x) for x in tup):
            return False

        # just too complicated
        if any(com.is_bool_indexer(x) for x in tup):
            return False

        return True
