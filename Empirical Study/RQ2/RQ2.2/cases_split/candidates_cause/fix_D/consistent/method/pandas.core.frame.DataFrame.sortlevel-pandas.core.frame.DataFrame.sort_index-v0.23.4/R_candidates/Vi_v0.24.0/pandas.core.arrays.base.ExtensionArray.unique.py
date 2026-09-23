    def unique(self):
        """
        Compute the ExtensionArray of unique values.

        Returns
        -------
        uniques : ExtensionArray
        """
        from pandas import unique

        uniques = unique(self.astype(object))
        return self._from_sequence(uniques, dtype=self.dtype)
