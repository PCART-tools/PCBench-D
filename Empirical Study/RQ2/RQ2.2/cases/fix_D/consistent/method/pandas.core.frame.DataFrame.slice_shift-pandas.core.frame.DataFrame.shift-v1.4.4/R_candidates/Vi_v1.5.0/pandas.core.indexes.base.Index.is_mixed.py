    @final
    def is_mixed(self) -> bool:
        """
        Check if the Index holds data with mixed data types.

        Returns
        -------
        bool
            Whether or not the Index holds data with mixed data types.

        See Also
        --------
        is_boolean : Check if the Index only consists of booleans.
        is_integer : Check if the Index only consists of integers.
        is_floating : Check if the Index is a floating type.
        is_numeric : Check if the Index only consists of numeric data.
        is_object : Check if the Index is of the object dtype.
        is_categorical : Check if the Index holds categorical data.
        is_interval : Check if the Index holds Interval objects.

        Examples
        --------
        >>> idx = pd.Index(['a', np.nan, 'b'])
        >>> idx.is_mixed()
        True

        >>> idx = pd.Index([1.0, 2.0, 3.0, 5.0])
        >>> idx.is_mixed()
        False
        """
        warnings.warn(
            "Index.is_mixed is deprecated and will be removed in a future version. "
            "Check index.inferred_type directly instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.inferred_type in ["mixed"]
