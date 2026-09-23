    def combine_first(self, other):
        """
        Combine Series values, choosing the calling Series's values
        first. Result index will be the union of the two indexes

        Parameters
        ----------
        other : Series

        Returns
        -------
        combined : Series

        Examples
        --------
        >>> s1 = pd.Series([1, np.nan])
        >>> s2 = pd.Series([3, 4])
        >>> s1.combine_first(s2)
        0    1.0
        1    4.0
        dtype: float64

        See Also
        --------
        Series.combine : Perform elementwise operation on two Series
            using a given function
        """
        new_index = self.index.union(other.index)
        this = self.reindex(new_index, copy=False)
        other = other.reindex(new_index, copy=False)
        # TODO: do we need name?
        name = ops.get_op_result_name(self, other)  # noqa
        rs_vals = com._where_compat(isna(this), other._values, this._values)
        return self._constructor(rs_vals, index=new_index).__finalize__(self)
