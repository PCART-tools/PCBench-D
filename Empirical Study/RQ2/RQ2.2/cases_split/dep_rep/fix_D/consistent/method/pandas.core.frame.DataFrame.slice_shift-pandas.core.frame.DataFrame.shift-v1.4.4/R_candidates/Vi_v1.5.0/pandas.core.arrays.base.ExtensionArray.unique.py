    def unique(self: ExtensionArrayT) -> ExtensionArrayT:
        """
        Compute the ExtensionArray of unique values.

        Returns
        -------
        uniques : ExtensionArray
        """
        uniques = unique(self.astype(object))
        return self._from_sequence(uniques, dtype=self.dtype)
