    def _box_item_values(self, key, values):
        items = self.columns[self.columns.get_loc(key)]
        if values.ndim == 2:
            return self._constructor(values.T, columns=items, index=self.index)
        else:
            return self._box_col_values(values, items)
