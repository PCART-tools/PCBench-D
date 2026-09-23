    def sym_diff(self, other, result_name=None):
        """
        Compute the sorted symmetric difference of two Index objects.

        Parameters
        ----------

        other : array-like
        result_name : str

        Returns
        -------
        sym_diff : Index

        Notes
        -----
        ``sym_diff`` contains elements that appear in either ``idx1`` or
        ``idx2`` but not both. Equivalent to the Index created by
        ``(idx1 - idx2) + (idx2 - idx1)`` with duplicates dropped.

        The sorting of a result containing ``NaN`` values is not guaranteed
        across Python versions. See GitHub issue #6444.

        Examples
        --------
        >>> idx1 = Index([1, 2, 3, 4])
        >>> idx2 = Index([2, 3, 4, 5])
        >>> idx1.sym_diff(idx2)
        Int64Index([1, 5], dtype='int64')

        You can also use the ``^`` operator:

        >>> idx1 ^ idx2
        Int64Index([1, 5], dtype='int64')
        """
        if not hasattr(other, '__iter__'):
            raise TypeError('Input must be iterable!')

        if not isinstance(other, Index):
            other = Index(other)
            result_name = result_name or self.name

        the_diff = sorted(set((self.difference(other)).union(other.difference(self))))
        return Index(the_diff, name=result_name)
