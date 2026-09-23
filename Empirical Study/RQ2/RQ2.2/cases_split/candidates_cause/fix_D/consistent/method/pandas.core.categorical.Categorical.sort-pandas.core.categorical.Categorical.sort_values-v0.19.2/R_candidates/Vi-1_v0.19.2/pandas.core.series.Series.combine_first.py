    def combine_first(self, other):
        """
        Combine Series values, choosing the calling Series's values
        first. Result index will be the union of the two indexes

        Parameters
        ----------
        other : Series

        Returns
        -------
        y : Series
        """
        new_index = self.index.union(other.index)
        this = self.reindex(new_index, copy=False)
        other = other.reindex(new_index, copy=False)
        # TODO: do we need name?
        name = _maybe_match_name(self, other)  # noqa
        rs_vals = com._where_compat(isnull(this), other._values, this._values)
        return self._constructor(rs_vals, index=new_index).__finalize__(self)
