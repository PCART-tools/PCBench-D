    @final
    def is_boolean(self) -> bool:
        """
        Check if the Index only consists of booleans.

        .. deprecated:: 2.0.0
            Use `pandas.api.types.is_bool_dtype` instead.

        Returns
        -------
        bool
            Whether or not the Index only consists of booleans.

        See Also
        --------
        is_integer : Check if the Index only consists of integers (deprecated).
        is_floating : Check if the Index is a floating type (deprecated).
        is_numeric : Check if the Index only consists of numeric data (deprecated).
        is_object : Check if the Index is of the object dtype (deprecated).
        is_categorical : Check if the Index holds categorical data.
        is_interval : Check if the Index holds Interval objects (deprecated).

        Examples
        --------
        >>> idx = pd.Index([True, False, True])
        >>> idx.is_boolean()  # doctest: +SKIP
        True

        >>> idx = pd.Index(["True", "False", "True"])
        >>> idx.is_boolean()  # doctest: +SKIP
        False

        >>> idx = pd.Index([True, False, "True"])
        >>> idx.is_boolean()  # doctest: +SKIP
        False
        """
        warnings.warn(
            f"{type(self).__name__}.is_boolean is deprecated. "
            "Use pandas.api.types.is_bool_type instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.inferred_type in ["boolean"]
