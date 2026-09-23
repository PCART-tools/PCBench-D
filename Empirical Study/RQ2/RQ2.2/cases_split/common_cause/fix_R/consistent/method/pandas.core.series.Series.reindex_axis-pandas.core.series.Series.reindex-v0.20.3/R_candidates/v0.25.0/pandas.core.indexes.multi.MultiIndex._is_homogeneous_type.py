    @property
    def _is_homogeneous_type(self):
        """Whether the levels of a MultiIndex all have the same dtype.

        This looks at the dtypes of the levels.

        See Also
        --------
        Index._is_homogeneous_type
        DataFrame._is_homogeneous_type

        Examples
        --------
        >>> MultiIndex.from_tuples([
        ...     ('a', 'b'), ('a', 'c')])._is_homogeneous_type
        True
        >>> MultiIndex.from_tuples([
        ...     ('a', 1), ('a', 2)])._is_homogeneous_type
        False
        """
        return len({x.dtype for x in self.levels}) <= 1
