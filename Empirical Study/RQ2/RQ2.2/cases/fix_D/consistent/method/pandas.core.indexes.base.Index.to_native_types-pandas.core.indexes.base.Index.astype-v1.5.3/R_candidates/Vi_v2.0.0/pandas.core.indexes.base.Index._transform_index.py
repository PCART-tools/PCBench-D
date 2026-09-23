    @final
    def _transform_index(self, func, *, level=None) -> Index:
        """
        Apply function to all values found in index.

        This includes transforming multiindex entries separately.
        Only apply function to one level of the MultiIndex if level is specified.
        """
        if isinstance(self, ABCMultiIndex):
            values = [
                self.get_level_values(i).map(func)
                if i == level or level is None
                else self.get_level_values(i)
                for i in range(self.nlevels)
            ]
            return type(self).from_arrays(values)
        else:
            items = [func(x) for x in self]
            return Index(items, name=self.name, tupleize_cols=False)
