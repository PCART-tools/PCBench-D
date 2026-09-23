    def _set_value(self, label, value, takeable=False):
        values = self.to_dense()

        # if the label doesn't exist, we will create a new object here
        # and possibily change the index
        new_values = values._set_value(label, value, takeable=takeable)
        if new_values is not None:
            values = new_values
        new_index = values.index
        values = SparseArray(values, fill_value=self.fill_value,
                             kind=self.kind)
        self._data = SingleBlockManager(values, new_index)
        self._index = new_index
