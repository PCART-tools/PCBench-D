    def all(self, *args, **kwargs):
        """
        Return whether all elements are Truthy.

        Parameters
        ----------
        *args
            Required for compatibility with numpy.
        **kwargs
            Required for compatibility with numpy.

        Returns
        -------
        bool or array-like (if axis is specified)
            A single element array-like may be converted to bool.

        See Also
        --------
        Index.any : Return whether any element in an Index is True.
        Series.any : Return whether any element in a Series is True.
        Series.all : Return whether all elements in a Series are True.

        Notes
        -----
        Not a Number (NaN), positive infinity and negative infinity
        evaluate to True because these are not equal to zero.

        Examples
        --------
        True, because nonzero integers are considered True.

        >>> pd.Index([1, 2, 3]).all()
        True

        False, because ``0`` is considered False.

        >>> pd.Index([0, 1, 2]).all()
        False
        """
        nv.validate_all(args, kwargs)
        self._maybe_disable_logical_methods("all")
        # error: Argument 1 to "all" has incompatible type "ArrayLike"; expected
        # "Union[Union[int, float, complex, str, bytes, generic], Sequence[Union[int,
        # float, complex, str, bytes, generic]], Sequence[Sequence[Any]],
        # _SupportsArray]"
        return np.all(self.values)  # type: ignore[arg-type]
