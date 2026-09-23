    def searchsorted(self, v, side='left', sorter=None):
        """Find indices where elements should be inserted to maintain order.

        Find the indices into a sorted Series `self` such that, if the
        corresponding elements in `v` were inserted before the indices, the
        order of `self` would be preserved.

        Parameters
        ----------
        v : array_like
            Values to insert into `a`.
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
        Series.sort
        Series.order
        numpy.searchsorted

        Notes
        -----
        Binary search is used to find the required insertion points.

        Examples
        --------
        >>> x = pd.Series([1, 2, 3])
        >>> x
        0    1
        1    2
        2    3
        dtype: int64
        >>> x.searchsorted(4)
        array([3])
        >>> x.searchsorted([0, 4])
        array([0, 3])
        >>> x.searchsorted([1, 3], side='left')
        array([0, 2])
        >>> x.searchsorted([1, 3], side='right')
        array([1, 3])
        >>> x.searchsorted([1, 2], side='right', sorter=[0, 2, 1])
        array([1, 3])
        """
        if sorter is not None:
            sorter = com._ensure_platform_int(sorter)

        return self.values.searchsorted(Series(v).values, side=side,
                                        sorter=sorter)
