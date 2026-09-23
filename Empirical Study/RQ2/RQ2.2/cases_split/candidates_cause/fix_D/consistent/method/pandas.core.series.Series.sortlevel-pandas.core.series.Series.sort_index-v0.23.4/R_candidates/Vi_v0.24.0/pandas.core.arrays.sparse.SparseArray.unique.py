    def unique(self):
        uniques = list(algos.unique(self.sp_values))
        fill_loc = self._first_fill_value_loc()
        if fill_loc >= 0:
            uniques.insert(fill_loc, self.fill_value)
        return type(self)._from_sequence(uniques, dtype=self.dtype)
