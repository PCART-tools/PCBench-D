    def searchsorted(self, v, side='left', sorter=None):
        """Find indices where elements should be inserted to maintain order.

        Find the indices into a sorted Categorical `self` such that, if the
        corresponding elements in `v` were inserted before the indices, the
        order of `self` would be preserved.

        Parameters
        ----------
        v : array_like
            Array-like values or a scalar value, to insert/search for in `self`.
        side : {'left', 'right'}, optional
            If 'left', the index of the first suitable location found is given.
            If 'right', return the last such index.  If there is no suitable
            index, return either 0 or N (where N is the length of `a`).
        sorter : 1-D array_like, optional
            Optional array of integer indices that sort `self` into ascending
            order. They are typically the result of ``np.argsort``.

        Returns
        -------
        indices : array of ints
            Array of insertion points with the same shape as `v`.

        See Also
        --------
        Series.searchsorted
        numpy.searchsorted

        Notes
        -----
        Binary search is used to find the required insertion points.

        Examples
        --------
        >>> x = pd.Categorical(['apple', 'bread', 'bread', 'cheese', 'milk' ])
        [apple, bread, bread, cheese, milk]
        Categories (4, object): [apple < bread < cheese < milk]
        >>> x.searchsorted('bread')
        array([1])     # Note: an array, not a scalar
        >>> x.searchsorted(['bread'])
        array([1])
        >>> x.searchsorted(['bread', 'eggs'])
        array([1, 4])
        >>> x.searchsorted(['bread', 'eggs'], side='right')
        array([3, 4])	    # eggs before milk
        >>> x = pd.Categorical(['apple', 'bread', 'bread', 'cheese', 'milk', 'donuts' ])
        >>> x.searchsorted(['bread', 'eggs'], side='right', sorter=[0, 1, 2, 3, 5, 4])
        array([3, 5])       # eggs after donuts, after switching milk and donuts
        """
        if not self.ordered:
            raise ValueError("Categorical not ordered\n"
                             "you can use .as_ordered() to change the Categorical to an ordered one\n")

        from pandas.core.series import Series
        values_as_codes = self.categories.values.searchsorted(Series(v).values, side)
        return self.codes.searchsorted(values_as_codes, sorter=sorter)
