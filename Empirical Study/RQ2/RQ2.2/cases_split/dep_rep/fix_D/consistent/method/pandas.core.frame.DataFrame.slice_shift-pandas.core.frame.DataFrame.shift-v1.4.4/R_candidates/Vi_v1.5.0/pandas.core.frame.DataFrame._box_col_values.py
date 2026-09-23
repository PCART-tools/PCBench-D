    def _box_col_values(self, values: SingleDataManager, loc: int) -> Series:
        """
        Provide boxed values for a column.
        """
        # Lookup in columns so that if e.g. a str datetime was passed
        #  we attach the Timestamp object as the name.
        name = self.columns[loc]
        klass = self._constructor_sliced
        # We get index=self.index bc values is a SingleDataManager
        return klass(values, name=name, fastpath=True).__finalize__(self)
