    def any(self, *args, **kwargs):
        """
        Return whether any element is Truthy.

        Parameters
        ----------
        *args
            These parameters will be passed to numpy.any.
        **kwargs
            These parameters will be passed to numpy.any.

        Returns
        -------
        any : bool or array_like (if axis is specified)
            A single element array_like may be converted to bool.

        See Also
        --------
        Index.all : Return whether all elements are True.
        Series.all : Return whether all elements are True.

        Notes
        -----
        Not a Number (NaN), positive infinity and negative infinity
        evaluate to True because these are not equal to zero.

        Examples
        --------
        >>> index = pd.Index([0, 1, 2])
        >>> index.any()
        True

        >>> index = pd.Index([0, 0, 0])
        >>> index.any()
        False
        """
        # FIXME: docstr inaccurate, args/kwargs not passed
        self._maybe_disable_logical_methods("any")
        return np.any(self.values)
