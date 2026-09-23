    @property
    def _is_homogeneous_type(self) -> bool:
        """
        Whether all the columns in a DataFrame have the same type.

        Returns
        -------
        bool

        See Also
        --------
        Index._is_homogeneous_type : Whether the object has a single
            dtype.
        MultiIndex._is_homogeneous_type : Whether all the levels of a
            MultiIndex have the same dtype.

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
        if self._data.any_extension_types:
            return len({block.dtype for block in self._data.blocks}) == 1
        else:
            return not self._data.is_mixed_type
