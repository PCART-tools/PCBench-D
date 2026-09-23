    def apply(self, func, axis=0, broadcast=None, reduce=None, result_type=None):
        """
        Analogous to DataFrame.apply, for SparseDataFrame

        Parameters
        ----------
        func : function
            Function to apply to each column
        axis : {0, 1, 'index', 'columns'}
        broadcast : bool, default False
            For aggregation functions, return object of same size with values
            propagated

            .. deprecated:: 0.23.0
               This argument will be removed in a future version, replaced
               by result_type='broadcast'.

        reduce : boolean or None, default None
            Try to apply reduction procedures. If the DataFrame is empty,
            apply will use reduce to determine whether the result should be a
            Series or a DataFrame. If reduce is None (the default), apply's
            return value will be guessed by calling func an empty Series (note:
            while guessing, exceptions raised by func will be ignored). If
            reduce is True a Series will always be returned, and if False a
            DataFrame will always be returned.

            .. deprecated:: 0.23.0
               This argument will be removed in a future version, replaced
               by result_type='reduce'.

        result_type : {'expand', 'reduce', 'broadcast, None}
            These only act when axis=1 {columns}:

            * 'expand' : list-like results will be turned into columns.
            * 'reduce' : return a Series if possible rather than expanding
              list-like results. This is the opposite to 'expand'.
            * 'broadcast' : results will be broadcast to the original shape
              of the frame, the original index & columns will be retained.

            The default behaviour (None) depends on the return value of the
            applied function: list-like results will be returned as a Series
            of those. However if the apply function returns a Series these
            are expanded to columns.

            .. versionadded:: 0.23.0

        Returns
        -------
        applied : Series or SparseDataFrame
        """
        if not len(self.columns):
            return self
        axis = self._get_axis_number(axis)

        if isinstance(func, np.ufunc):
            new_series = {}
            for k, v in self.items():
                applied = func(v)
                applied.fill_value = func(v.fill_value)
                new_series[k] = applied
            return self._constructor(
                new_series,
                index=self.index,
                columns=self.columns,
                default_fill_value=self._default_fill_value,
                default_kind=self._default_kind,
            ).__finalize__(self)

        from pandas.core.apply import frame_apply

        op = frame_apply(
            self,
            func=func,
            axis=axis,
            reduce=reduce,
            broadcast=broadcast,
            result_type=result_type,
        )
        return op.get_result()
