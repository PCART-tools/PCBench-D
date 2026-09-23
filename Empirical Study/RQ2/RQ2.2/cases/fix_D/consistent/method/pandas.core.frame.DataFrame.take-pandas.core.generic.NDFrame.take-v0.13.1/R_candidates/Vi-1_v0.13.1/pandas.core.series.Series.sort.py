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
        Series.order
        """

        # GH 5856/5863
        if self._is_cached:
            raise ValueError("This Series is a view of some other array, to "
                             "sort in-place you must create a copy")

        result = self.order(na_last=True, kind=kind,
                            ascending=ascending)

        self._update_inplace(result)
