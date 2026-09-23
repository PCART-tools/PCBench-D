    @property
    def _is_homogeneous_type(self) -> bool:
        """
        Whether all the columns in a DataFrame have the same type.

        Returns
        -------
        bool

        Examples
        --------
        >>> DataFrame({"A": [1, 2], "B": [3, 4]})._is_homogeneous_type
        True
        >>> DataFrame({"A": [1, 2], "B": [3.0, 4.0]})._is_homogeneous_type
        False

        Items with the same type but different sizes are considered
        different types.

        >>> DataFrame({
        ...    "A": np.array([1, 2], dtype=np.int32),
        ...    "B": np.array([1, 2], dtype=np.int64)})._is_homogeneous_type
        False
        """
        # The "<" part of "<=" here is for empty DataFrame cases
        return len({arr.dtype for arr in self._mgr.arrays}) <= 1
