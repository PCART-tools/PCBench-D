    def fillna(self, value=None, method=None, axis=None, inplace=False,
               limit=None, downcast=None):
        """
        Fill NA/NaN values using the specified method.

        Parameters
        ----------
        value : scalar, dict, Series, or DataFrame
            Value to use to fill holes (e.g. 0), alternately a
            dict/Series/DataFrame of values specifying which value to use for
            each index (for a Series) or column (for a DataFrame). (values not
            in the dict/Series/DataFrame will not be filled). This value cannot
            be a list.
        method : {'backfill', 'bfill', 'pad', 'ffill', None}, default None
            Method to use for filling holes in reindexed Series
            pad / ffill: propagate last valid observation forward to next valid
            backfill / bfill: use NEXT valid observation to fill gap
        axis : %(axes_single_arg)s
        inplace : boolean, default False
            If True, fill in place. Note: this will modify any
            other views on this object, (e.g. a no-copy slice for a column in a
            DataFrame).
        limit : int, default None
            If method is specified, this is the maximum number of consecutive
            NaN values to forward/backward fill. In other words, if there is
            a gap with more than this number of consecutive NaNs, it will only
            be partially filled. If method is not specified, this is the
            maximum number of entries along the entire axis where NaNs will be
            filled. Must be greater than 0 if not None.
        downcast : dict, default is None
            a dict of item->dtype of what to downcast if possible,
            or the string 'infer' which will try to downcast to an appropriate
            equal type (e.g. float64 to int64 if possible)

        Returns
        -------
        filled : %(klass)s

        See Also
        --------
        interpolate : Fill NaN values using interpolation.
        reindex, asfreq

        Examples
        --------
        >>> df = pd.DataFrame([[np.nan, 2, np.nan, 0],
        ...                    [3, 4, np.nan, 1],
        ...                    [np.nan, np.nan, np.nan, 5],
        ...                    [np.nan, 3, np.nan, 4]],
        ...                    columns=list('ABCD'))
        >>> df
             A    B   C  D
        0  NaN  2.0 NaN  0
        1  3.0  4.0 NaN  1
        2  NaN  NaN NaN  5
        3  NaN  3.0 NaN  4

        Replace all NaN elements with 0s.

        >>> df.fillna(0)
            A   B   C   D
        0   0.0 2.0 0.0 0
        1   3.0 4.0 0.0 1
        2   0.0 0.0 0.0 5
        3   0.0 3.0 0.0 4

        We can also propagate non-null values forward or backward.

        >>> df.fillna(method='ffill')
            A   B   C   D
        0   NaN 2.0 NaN 0
        1   3.0 4.0 NaN 1
        2   3.0 4.0 NaN 5
        3   3.0 3.0 NaN 4

        Replace all NaN elements in column 'A', 'B', 'C', and 'D', with 0, 1,
        2, and 3 respectively.

        >>> values = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        >>> df.fillna(value=values)
            A   B   C   D
        0   0.0 2.0 2.0 0
        1   3.0 4.0 2.0 1
        2   0.0 1.0 2.0 5
        3   0.0 3.0 2.0 4

        Only replace the first NaN element.

        >>> df.fillna(value=values, limit=1)
            A   B   C   D
        0   0.0 2.0 2.0 0
        1   3.0 4.0 NaN 1
        2   NaN 1.0 NaN 5
        3   NaN 3.0 NaN 4
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        value, method = validate_fillna_kwargs(value, method)

        self._consolidate_inplace()

        # set the default here, so functions examining the signaure
        # can detect if something was set (e.g. in groupby) (GH9221)
        if axis is None:
            axis = 0
        axis = self._get_axis_number(axis)

        from pandas import DataFrame
        if value is None:

            if self._is_mixed_type and axis == 1:
                if inplace:
                    raise NotImplementedError()
                result = self.T.fillna(method=method, limit=limit).T

                # need to downcast here because of all of the transposes
                result._data = result._data.downcast()

                return result

            # > 3d
            if self.ndim > 3:
                raise NotImplementedError('Cannot fillna with a method for > '
                                          '3dims')

            # 3d
            elif self.ndim == 3:
                # fill in 2d chunks
                result = {col: s.fillna(method=method, value=value)
                          for col, s in self.iteritems()}
                prelim_obj = self._constructor.from_dict(result)
                new_obj = prelim_obj.__finalize__(self)
                new_data = new_obj._data

            else:
                # 2d or less
                new_data = self._data.interpolate(method=method, axis=axis,
                                                  limit=limit, inplace=inplace,
                                                  coerce=True,
                                                  downcast=downcast)
        else:
            if len(self._get_axis(axis)) == 0:
                return self

            if self.ndim == 1:
                if isinstance(value, (dict, ABCSeries)):
                    from pandas import Series
                    value = Series(value)
                elif not is_list_like(value):
                    pass
                else:
                    raise TypeError('"value" parameter must be a scalar, dict '
                                    'or Series, but you passed a '
                                    '"{0}"'.format(type(value).__name__))

                new_data = self._data.fillna(value=value, limit=limit,
                                             inplace=inplace,
                                             downcast=downcast)

            elif isinstance(value, (dict, ABCSeries)):
                if axis == 1:
                    raise NotImplementedError('Currently only can fill '
                                              'with dict/Series column '
                                              'by column')

                result = self if inplace else self.copy()
                for k, v in compat.iteritems(value):
                    if k not in result:
                        continue
                    obj = result[k]
                    obj.fillna(v, limit=limit, inplace=True, downcast=downcast)
                return result if not inplace else None

            elif not is_list_like(value):
                new_data = self._data.fillna(value=value, limit=limit,
                                             inplace=inplace,
                                             downcast=downcast)
            elif isinstance(value, DataFrame) and self.ndim == 2:
                new_data = self.where(self.notna(), value)
            else:
                raise ValueError("invalid fill value with a %s" % type(value))

        if inplace:
            self._update_inplace(new_data)
        else:
            return self._constructor(new_data).__finalize__(self)
