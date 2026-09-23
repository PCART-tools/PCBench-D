    def all(self):
        """
        Return whether all elements are Truthy.

        Parameters
        ----------
        *args
            These parameters will be passed to numpy.all.
        **kwargs
            These parameters will be passed to numpy.all.

        Returns
        -------
        all : bool or array_like (if axis is specified)
            A single element array_like may be converted to bool.

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
        **all**

        True, because nonzero integers are considered True.

        >>> pd.Index([1, 2, 3]).all()
        True

        False, because ``0`` is considered False.

        >>> pd.Index([0, 1, 2]).all()
        False

        **any**

        True, because ``1`` is considered True.

        >>> pd.Index([0, 0, 1]).any()
        True

        False, because ``0`` is considered False.

        >>> pd.Index([0, 0, 0]).any()
        False
        """
        # FIXME: docstr inaccurate, args/kwargs not passed

        self._maybe_disable_logical_methods("all")
        return np.all(self.values)
