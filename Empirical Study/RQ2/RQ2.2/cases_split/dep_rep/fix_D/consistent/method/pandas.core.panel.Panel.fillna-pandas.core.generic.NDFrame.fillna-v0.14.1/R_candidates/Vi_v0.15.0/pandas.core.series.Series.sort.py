    def sort(self, axis=0, ascending=True, kind='quicksort', na_position='last', inplace=True):
        """
        Sort values and index labels by value. This is an inplace sort by default.
        Series.order is the equivalent but returns a new Series.

        Parameters
        ----------
        axis : int (can only be zero)
        ascending : boolean, default True
            Sort ascending. Passing False sorts descending
        kind : {'mergesort', 'quicksort', 'heapsort'}, default 'quicksort'
            Choice of sorting algorithm. See np.sort for more
            information. 'mergesort' is the only stable algorithm
        na_position : {'first', 'last'} (optional, default='last')
            'first' puts NaNs at the beginning
            'last' puts NaNs at the end
        inplace : boolean, default True
            Do operation in place.

        See Also
        --------
        Series.order
        """
        return self.order(ascending=ascending,
                          kind=kind,
                          na_position=na_position,
                          inplace=inplace)
