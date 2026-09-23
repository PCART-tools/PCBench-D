    def fillna(self, value=None, method=None, axis=0, inplace=False,
               limit=None, downcast=None):
        """
        Fill NA/NaN values using the specified method

        Parameters
        ----------
        method : {'backfill', 'bfill', 'pad', 'ffill', None}, default None
            Method to use for filling holes in reindexed Series
            pad / ffill: propagate last valid observation forward to next valid
            backfill / bfill: use NEXT valid observation to fill gap
        value : scalar, dict, or Series
            Value to use to fill holes (e.g. 0), alternately a dict/Series of
            values specifying which value to use for each index (for a Series) or
            column (for a DataFrame). (values not in the dict/Series will not be
            filled). This value cannot be a list.
        axis : {0, 1}, default 0
            0: fill column-by-column
            1: fill row-by-row
        inplace : boolean, default False
            If True, fill in place. Note: this will modify any
            other views on this object, (e.g. a no-copy slice for a column in a
            DataFrame).
        limit : int, default None
            Maximum size gap to forward or backward fill
        downcast : dict, default is None
            a dict of item->dtype of what to downcast if possible,
            or the string 'infer' which will try to downcast to an appropriate
            equal type (e.g. float64 to int64 if possible)

        See also
        --------
        reindex, asfreq

        Returns
        -------
        filled : same type as caller
        """
        if isinstance(value, (list, tuple)):
            raise TypeError('"value" parameter must be a scalar or dict, but '
                            'you passed a "{0}"'.format(type(value).__name__))
        self._consolidate_inplace()

        axis = self._get_axis_number(axis)
        method = com._clean_fill_method(method)

        if value is None:
            if method is None:
                raise ValueError('must specify a fill method or value')
            if self._is_mixed_type and axis == 1:
                if inplace:
                    raise NotImplementedError()
                result = self.T.fillna(method=method, limit=limit).T

                # need to downcast here because of all of the transposes
                result._data = result._data.downcast()

                return result

            # > 3d
            if self.ndim > 3:
                raise NotImplementedError(
                    'Cannot fillna with a method for > 3dims'
                )

            # 3d
            elif self.ndim == 3:

                # fill in 2d chunks
                result = dict([(col, s.fillna(method=method, value=value))
                               for col, s in compat.iteritems(self)])
                return self._constructor.from_dict(result).__finalize__(self)

            # 2d or less
            method = com._clean_fill_method(method)
            new_data = self._data.interpolate(method=method,
                                              axis=axis,
                                              limit=limit,
                                              inplace=inplace,
                                              coerce=True,
                                              downcast=downcast)
        else:
            if method is not None:
                raise ValueError('cannot specify both a fill method and value')

            if len(self._get_axis(axis)) == 0:
                return self

            if self.ndim == 1 and value is not None:
                if isinstance(value, (dict, com.ABCSeries)):
                    from pandas import Series
                    value = Series(value)

                new_data = self._data.fillna(value, inplace=inplace,
                                             downcast=downcast)

            elif isinstance(value, (dict, com.ABCSeries)):
                if axis == 1:
                    raise NotImplementedError('Currently only can fill '
                                              'with dict/Series column '
                                              'by column')

                result = self if inplace else self.copy()
                for k, v in compat.iteritems(value):
                    if k not in result:
                        continue
                    obj = result[k]
                    obj.fillna(v, inplace=True)
                return result
            else:
                new_data = self._data.fillna(value, inplace=inplace,
                                             downcast=downcast)

        if inplace:
            self._update_inplace(new_data)
        else:
            return self._constructor(new_data).__finalize__(self)
