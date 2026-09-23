    def _internal_get_values(self):
        """
        Return `Index` data as an `numpy.ndarray`.

        Returns
        -------
        numpy.ndarray
            A one-dimensional numpy array of the `Index` values.

        See Also
        --------
        Index.values : The attribute that _internal_get_values wraps.

        Examples
        --------
        Getting the `Index` values of a `DataFrame`:

        >>> df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        ...                    index=['a', 'b', 'c'], columns=['A', 'B', 'C'])
        >>> df
           A  B  C
        a  1  2  3
        b  4  5  6
        c  7  8  9
        >>> df.index._internal_get_values()
        array(['a', 'b', 'c'], dtype=object)

        Standalone `Index` values:

        >>> idx = pd.Index(['1', '2', '3'])
        >>> idx._internal_get_values()
        array(['1', '2', '3'], dtype=object)

        `MultiIndex` arrays also have only one dimension:

        >>> midx = pd.MultiIndex.from_arrays([[1, 2, 3], ['a', 'b', 'c']],
        ...                                  names=('number', 'letter'))
        >>> midx._internal_get_values()
        array([(1, 'a'), (2, 'b'), (3, 'c')], dtype=object)
        >>> midx._internal_get_values().ndim
        1
        """
        return self.values
