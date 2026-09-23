    def fillna(self, value=None, method=None):
        """
        Fill NaN values using the specified method.

        Member Series / TimeSeries are filled separately.

        Parameters
        ----------
        value : any kind (should be same type as array)
            Value to use to fill holes (e.g. 0)

        method : {'backfill', 'bfill', 'pad', 'ffill', None}, default 'pad'
            Method to use for filling holes in reindexed Series

            pad / ffill: propagate last valid observation forward to next valid
            backfill / bfill: use NEXT valid observation to fill gap

        Returns
        -------
        y : DataFrame

        See also
        --------
        DataFrame.reindex, DataFrame.asfreq
        """
        if isinstance(value, (list, tuple)):
            raise TypeError('"value" parameter must be a scalar or dict, but '
                            'you passed a "{0}"'.format(type(value).__name__))
        if value is None:
            if method is None:
                raise ValueError('must specify a fill method or value')
            result = {}
            for col, s in self.iterkv():
                result[col] = s.fillna(method=method, value=value)

            return self._constructor.from_dict(result)
        else:
            if method is not None:
                raise ValueError('cannot specify both a fill method and value')
            new_data = self._data.fillna(value)
            return self._constructor(new_data)
