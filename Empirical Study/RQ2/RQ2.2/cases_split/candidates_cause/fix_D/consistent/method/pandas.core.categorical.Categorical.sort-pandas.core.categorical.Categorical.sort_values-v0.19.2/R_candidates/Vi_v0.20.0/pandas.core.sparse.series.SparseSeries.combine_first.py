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
        if isinstance(other, SparseSeries):
            other = other.to_dense()

        dense_combined = self.to_dense().combine_first(other)
        return dense_combined.to_sparse(fill_value=self.fill_value)
