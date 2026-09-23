    @final
    def is_object(self) -> bool:
        """
        Check if the Index is of the object dtype.

        .. deprecated:: 2.0.0
           Use `pandas.api.types.is_object_dtype` instead.

        Returns
        -------
        bool
            Whether or not the Index is of the object dtype.

        See Also
        --------
        is_boolean : Check if the Index only consists of booleans (deprecated).
        is_integer : Check if the Index only consists of integers (deprecated).
        is_floating : Check if the Index is a floating type (deprecated).
        is_numeric : Check if the Index only consists of numeric data (deprecated).
        is_categorical : Check if the Index holds categorical data (deprecated).
        is_interval : Check if the Index holds Interval objects (deprecated).

        Examples
        --------
        >>> idx = pd.Index(["Apple", "Mango", "Watermelon"])
        >>> idx.is_object()  # doctest: +SKIP
        True

        >>> idx = pd.Index(["Apple", "Mango", 2.0])
        >>> idx.is_object()  # doctest: +SKIP
        True

        >>> idx = pd.Index(["Watermelon", "Orange", "Apple",
        ...                 "Watermelon"]).astype("category")
        >>> idx.is_object()  # doctest: +SKIP
        False

        >>> idx = pd.Index([1.0, 2.0, 3.0, 4.0])
        >>> idx.is_object()  # doctest: +SKIP
        False
        """
        warnings.warn(
            f"{type(self).__name__}.is_object is deprecated."
            "Use pandas.api.types.is_object_dtype instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return is_object_dtype(self.dtype)
