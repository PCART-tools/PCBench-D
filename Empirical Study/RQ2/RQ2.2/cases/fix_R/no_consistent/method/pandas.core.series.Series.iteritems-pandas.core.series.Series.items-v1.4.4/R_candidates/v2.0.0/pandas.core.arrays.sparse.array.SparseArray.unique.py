    def unique(self: SparseArrayT) -> SparseArrayT:
        uniques = algos.unique(self.sp_values)
        if len(self.sp_values) != len(self):
            fill_loc = self._first_fill_value_loc()
            # Inorder to align the behavior of pd.unique or
            # pd.Series.unique, we should keep the original
            # order, here we use unique again to find the
            # insertion place. Since the length of sp_values
            # is not large, maybe minor performance hurt
            # is worthwhile to the correctness.
            insert_loc = len(algos.unique(self.sp_values[:fill_loc]))
            uniques = np.insert(uniques, insert_loc, self.fill_value)
        return type(self)._from_sequence(uniques, dtype=self.dtype)
