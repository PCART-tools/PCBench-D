    def _box_col_values(self, values, items):
        """
        Provide boxed values for a column.
        """
        klass = self._constructor_sliced
        return klass(values, index=self.index, name=items, fastpath=True)
