    def rename(
        self,
        index=None,
        *,
        axis=None,
        copy=True,
        inplace=False,
        level=None,
        errors="ignore",
    ) -> Series | None:
        """
        Alter Series index labels or name.

        Function / dict values must be unique (1-to-1). Labels not contained in
        a dict / Series will be left as-is. Extra labels listed don't throw an
        error.

        Alternatively, change ``Series.name`` with a scalar value.

        See the :ref:`user guide <basics.rename>` for more.

        Parameters
        ----------
        axis : {0 or "index"}
            Unused. Accepted for compatibility with DataFrame method only.
        index : scalar, hashable sequence, dict-like or function, optional
            Functions or dict-like are transformations to apply to
            the index.
            Scalar or hashable sequence-like will alter the ``Series.name``
            attribute.

        **kwargs
            Additional keyword arguments passed to the function. Only the
            "inplace" keyword is used.

        Returns
        -------
        Series or None
            Series with index labels or name altered or None if ``inplace=True``.

        See Also
        --------
        DataFrame.rename : Corresponding DataFrame method.
        Series.rename_axis : Set the name of the axis.

        Examples
        --------
        >>> s = pd.Series([1, 2, 3])
        >>> s
        0    1
        1    2
        2    3
        dtype: int64
        >>> s.rename("my_name")  # scalar, changes Series.name
        0    1
        1    2
        2    3
        Name: my_name, dtype: int64
        >>> s.rename(lambda x: x ** 2)  # function, changes labels
        0    1
        1    2
        4    3
        dtype: int64
        >>> s.rename({1: 3, 2: 5})  # mapping, changes labels
        0    1
        3    2
        5    3
        dtype: int64
        """
        if axis is not None:
            # Make sure we raise if an invalid 'axis' is passed.
            axis = self._get_axis_number(axis)

        if callable(index) or is_dict_like(index):
            return super()._rename(
                index, copy=copy, inplace=inplace, level=level, errors=errors
            )
        else:
            return self._set_name(index, inplace=inplace)
