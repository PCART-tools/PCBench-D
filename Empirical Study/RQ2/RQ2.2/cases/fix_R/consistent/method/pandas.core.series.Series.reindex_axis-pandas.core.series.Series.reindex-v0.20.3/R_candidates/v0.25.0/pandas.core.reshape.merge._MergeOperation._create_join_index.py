    def _create_join_index(
        self, index, other_index, indexer, other_indexer, how="left"
    ):
        """
        Create a join index by rearranging one index to match another

        Parameters
        ----------
        index: Index being rearranged
        other_index: Index used to supply values not found in index
        indexer: how to rearrange index
        how: replacement is only necessary if indexer based on other_index

        Returns
        -------
        join_index
        """
        if self.how in (how, "outer") and not isinstance(other_index, MultiIndex):
            # if final index requires values in other_index but not target
            # index, indexer may hold missing (-1) values, causing Index.take
            # to take the final value in target index. So, we set the last
            # element to be the desired fill value. We do not use allow_fill
            # and fill_value because it throws a ValueError on integer indices
            mask = indexer == -1
            if np.any(mask):
                fill_value = na_value_for_dtype(index.dtype, compat=False)
                index = index.append(Index([fill_value]))
        return index.take(indexer)
