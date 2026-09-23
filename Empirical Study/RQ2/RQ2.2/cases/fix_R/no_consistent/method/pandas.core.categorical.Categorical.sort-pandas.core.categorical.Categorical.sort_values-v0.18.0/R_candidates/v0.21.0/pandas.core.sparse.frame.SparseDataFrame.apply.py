    def apply(self, func, axis=0, broadcast=False, reduce=False):
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

        Returns
        -------
        applied : Series or SparseDataFrame
        """
        if not len(self.columns):
            return self
        axis = self._get_axis_number(axis)

        if isinstance(func, np.ufunc):
            new_series = {}
            for k, v in compat.iteritems(self):
                applied = func(v)
                applied.fill_value = func(v.fill_value)
                new_series[k] = applied
            return self._constructor(
                new_series, index=self.index, columns=self.columns,
                default_fill_value=self._default_fill_value,
                default_kind=self._default_kind).__finalize__(self)
        else:
            if not broadcast:
                return self._apply_standard(func, axis, reduce=reduce)
            else:
                return self._apply_broadcast(func, axis)
