    def combine(self, other, func, fill_value=np.nan):
        """
        Perform elementwise binary operation on two Series using given function
        with optional fill value when an index is missing from one Series or
        the other

        Parameters
        ----------
        other : Series or scalar value
        func : function
            Function that takes two scalars as inputs and return a scalar
        fill_value : scalar value

        Returns
        -------
        result : Series

        Examples
        --------
        >>> s1 = Series([1, 2])
        >>> s2 = Series([0, 3])
        >>> s1.combine(s2, lambda x1, x2: x1 if x1 < x2 else x2)
        0    0
        1    2
        dtype: int64

        See Also
        --------
        Series.combine_first : Combine Series values, choosing the calling
            Series's values first
        """
        if isinstance(other, Series):
            new_index = self.index.union(other.index)
            new_name = ops.get_op_result_name(self, other)
            new_values = np.empty(len(new_index), dtype=self.dtype)
            for i, idx in enumerate(new_index):
                lv = self.get(idx, fill_value)
                rv = other.get(idx, fill_value)
                with np.errstate(all='ignore'):
                    new_values[i] = func(lv, rv)
        else:
            new_index = self.index
            with np.errstate(all='ignore'):
                new_values = func(self._values, other)
            new_name = self.name
        return self._constructor(new_values, index=new_index, name=new_name)
