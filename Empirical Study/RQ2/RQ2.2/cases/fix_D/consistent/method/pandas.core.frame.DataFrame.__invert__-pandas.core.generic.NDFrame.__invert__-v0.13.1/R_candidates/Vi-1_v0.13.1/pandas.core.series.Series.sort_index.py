    def sort_index(self, ascending=True):
        """
        Sort object by labels (along an axis)

        Parameters
        ----------
        ascending : boolean or list, default True
            Sort ascending vs. descending. Specify list for multiple sort
            orders

        Examples
        --------
        >>> result1 = s.sort_index(ascending=False)
        >>> result2 = s.sort_index(ascending=[1, 0])

        Returns
        -------
        sorted_obj : Series
        """
        index = self.index
        if isinstance(index, MultiIndex):
            from pandas.core.groupby import _lexsort_indexer
            indexer = _lexsort_indexer(index.labels, orders=ascending)
            indexer = com._ensure_platform_int(indexer)
            new_labels = index.take(indexer)
        else:
            new_labels, indexer = index.order(return_indexer=True,
                                              ascending=ascending)

        new_values = self.values.take(indexer)
        return self._constructor(new_values,
                                 index=new_labels).__finalize__(self)
