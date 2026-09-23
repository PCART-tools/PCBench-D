    def _box_col_values(self, values: SingleDataManager, loc: int) -> Series:
        """
        Provide boxed values for a column.
        """
        # Lookup in columns so that if e.g. a str datetime was passed
        #  we attach the Timestamp object as the name.
        name = self.columns[loc]
        # We get index=self.index bc values is a SingleDataManager
        obj = self._constructor_sliced_from_mgr(values, axes=values.axes)
        obj._name = name
        return obj.__finalize__(self)
