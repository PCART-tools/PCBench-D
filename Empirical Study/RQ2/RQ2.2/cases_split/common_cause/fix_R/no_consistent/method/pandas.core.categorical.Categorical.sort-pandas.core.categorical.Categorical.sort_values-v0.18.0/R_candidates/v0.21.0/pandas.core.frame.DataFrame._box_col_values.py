    def _box_col_values(self, values, items):
        """ provide boxed values for a column """
        return self._constructor_sliced.from_array(values, index=self.index,
                                                   name=items, fastpath=True)
