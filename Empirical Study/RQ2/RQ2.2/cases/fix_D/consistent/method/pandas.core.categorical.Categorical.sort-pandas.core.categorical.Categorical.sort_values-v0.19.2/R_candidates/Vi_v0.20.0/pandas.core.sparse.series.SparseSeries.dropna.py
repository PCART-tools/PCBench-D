    def dropna(self, axis=0, inplace=False, **kwargs):
        """
        Analogous to Series.dropna. If fill_value=NaN, returns a dense Series
        """
        # TODO: make more efficient
        axis = self._get_axis_number(axis or 0)
        dense_valid = self.to_dense().valid()
        if inplace:
            raise NotImplementedError("Cannot perform inplace dropna"
                                      " operations on a SparseSeries")
        if isnull(self.fill_value):
            return dense_valid
        else:
            dense_valid = dense_valid[dense_valid != self.fill_value]
            return dense_valid.to_sparse(fill_value=self.fill_value)
