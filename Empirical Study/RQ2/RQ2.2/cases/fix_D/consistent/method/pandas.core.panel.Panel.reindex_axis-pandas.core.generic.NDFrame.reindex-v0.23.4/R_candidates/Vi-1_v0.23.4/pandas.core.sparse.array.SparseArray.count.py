    def count(self):
        """
        Compute sum of non-NA/null observations in SparseArray. If the
        fill_value is not NaN, the "sparse" locations will be included in the
        observation count.

        Returns
        -------
        nobs : int
        """
        sp_values = self.sp_values
        valid_spvals = np.isfinite(sp_values).sum()
        if self._null_fill_value:
            return valid_spvals
        else:
            return valid_spvals + self.sp_index.ngaps
