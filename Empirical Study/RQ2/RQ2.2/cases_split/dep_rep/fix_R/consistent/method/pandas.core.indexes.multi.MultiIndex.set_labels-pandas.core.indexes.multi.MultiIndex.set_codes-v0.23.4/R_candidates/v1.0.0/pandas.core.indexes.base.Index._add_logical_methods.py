    @classmethod
    def _add_logical_methods(cls):
        """
        Add in logical methods.
        """
        _doc = """
        %(desc)s

        Parameters
        ----------
        *args
            These parameters will be passed to numpy.%(outname)s.
        **kwargs
            These parameters will be passed to numpy.%(outname)s.

        Returns
        -------
        %(outname)s : bool or array_like (if axis is specified)
            A single element array_like may be converted to bool."""

        _index_shared_docs["index_all"] = dedent(
            """

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
        )

        _index_shared_docs["index_any"] = dedent(
            """

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
        )

        def _make_logical_function(name, desc, f):
            @Substitution(outname=name, desc=desc)
            @Appender(_index_shared_docs["index_" + name])
            @Appender(_doc)
            def logical_func(self, *args, **kwargs):
                result = f(self.values)
                if (
                    isinstance(result, (np.ndarray, ABCSeries, Index))
                    and result.ndim == 0
                ):
                    # return NumPy type
                    return result.dtype.type(result.item())
                else:  # pragma: no cover
                    return result

            logical_func.__name__ = name
            return logical_func

        cls.all = _make_logical_function(
            "all", "Return whether all elements are True.", np.all
        )
        cls.any = _make_logical_function(
            "any", "Return whether any element is True.", np.any
        )
