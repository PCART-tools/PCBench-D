    def rename_axis(self, mapper, axis=0, copy=True, inplace=False):
        """
        Alter the name of the index or columns.

        Parameters
        ----------
        mapper : scalar, list-like, optional
            Value to set as the axis name attribute.
        axis : {0 or 'index', 1 or 'columns'}, default 0
            The index or the name of the axis.
        copy : boolean, default True
            Also copy underlying data.
        inplace : boolean, default False
            Modifies the object directly, instead of creating a new Series
            or DataFrame.

        Returns
        -------
        renamed : Series, DataFrame, or None
            The same type as the caller or None if `inplace` is True.

        Notes
        -----
        Prior to version 0.21.0, ``rename_axis`` could also be used to change
        the axis *labels* by passing a mapping or scalar. This behavior is
        deprecated and will be removed in a future version. Use ``rename``
        instead.

        See Also
        --------
        pandas.Series.rename : Alter Series index labels or name
        pandas.DataFrame.rename : Alter DataFrame index labels or name
        pandas.Index.rename : Set new names on index

        Examples
        --------
        **Series**

        >>> s = pd.Series([1, 2, 3])
        >>> s.rename_axis("foo")
        foo
        0    1
        1    2
        2    3
        dtype: int64

        **DataFrame**

        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        >>> df.rename_axis("foo")
             A  B
        foo
        0    1  4
        1    2  5
        2    3  6

        >>> df.rename_axis("bar", axis="columns")
        bar  A  B
        0    1  4
        1    2  5
        2    3  6
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        non_mapper = is_scalar(mapper) or (is_list_like(mapper) and not
                                           is_dict_like(mapper))
        if non_mapper:
            return self._set_axis_name(mapper, axis=axis, inplace=inplace)
        else:
            msg = ("Using 'rename_axis' to alter labels is deprecated. "
                   "Use '.rename' instead")
            warnings.warn(msg, FutureWarning, stacklevel=2)
            axis = self._get_axis_name(axis)
            d = {'copy': copy, 'inplace': inplace}
            d[axis] = mapper
            return self.rename(**d)
