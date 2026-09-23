    def value_counts(self, dropna=True):
        """
        Returns a Series containing counts of unique values.

        Parameters
        ----------
        dropna : boolean, default True
            Don't include counts of NaN, even if NaN is in sp_values.

        Returns
        -------
        counts : Series
        """
        keys, counts = algos._value_counts_arraylike(self.sp_values,
                                                     dropna=dropna)
        fcounts = self.sp_index.ngaps
        if fcounts > 0:
            if self._null_fill_value and dropna:
                pass
            else:
                if self._null_fill_value:
                    mask = pd.isna(keys)
                else:
                    mask = keys == self.fill_value

                if mask.any():
                    counts[mask] += fcounts
                else:
                    keys = np.insert(keys, 0, self.fill_value)
                    counts = np.insert(counts, 0, fcounts)

        if not isinstance(keys, pd.Index):
            keys = pd.Index(keys)
        result = pd.Series(counts, index=keys)
        return result
