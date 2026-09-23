    def sort(self, axis=0, kind='quicksort', order=None, ascending=True):
        """
        Sort values and index labels by value, in place. For compatibility with
        ndarray API. No return value

        Parameters
        ----------
        axis : int (can only be zero)
        kind : {'mergesort', 'quicksort', 'heapsort'}, default 'quicksort'
            Choice of sorting algorithm. See np.sort for more
            information. 'mergesort' is the only stable algorithm
        order : ignored
        ascending : boolean, default True
            Sort ascending. Passing False sorts descending

        See Also
        --------
        pandas.Series.order
        """
        sortedSeries = self.order(na_last=True, kind=kind,
                                  ascending=ascending)

        true_base = self.values
        while true_base.base is not None:
            true_base = true_base.base

        if (true_base is not None and
                (true_base.ndim != 1 or true_base.shape != self.shape)):
            raise TypeError('This Series is a view of some other array, to '
                            'sort in-place you must create a copy')

        self._data = sortedSeries._data.copy()
        self.index = sortedSeries.index
