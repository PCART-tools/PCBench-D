    def order(self, na_last=None, ascending=True, kind='quicksort',
              na_position='last', inplace=False):
        """
        DEPRECATED: use :meth:`Series.sort_values`

        Sorts Series object, by value, maintaining index-value link.
        This will return a new Series by default. Series.sort is the equivalent
        but as an inplace method.

        Parameters
        ----------
        na_last : boolean (optional, default=True)--DEPRECATED; use na_position
            Put NaN's at beginning or end
        ascending : boolean, default True
            Sort ascending. Passing False sorts descending
        kind : {'mergesort', 'quicksort', 'heapsort'}, default 'quicksort'
            Choice of sorting algorithm. See np.sort for more
            information. 'mergesort' is the only stable algorithm
        na_position : {'first', 'last'} (optional, default='last')
            'first' puts NaNs at the beginning
            'last' puts NaNs at the end
        inplace : boolean, default False
            Do operation in place.

        Returns
        -------
        y : Series

        See Also
        --------
        Series.sort_values
        """
        warnings.warn("order is deprecated, use sort_values(...)",
                      FutureWarning, stacklevel=2)

        return self.sort_values(ascending=ascending, kind=kind,
                                na_position=na_position, inplace=inplace)
