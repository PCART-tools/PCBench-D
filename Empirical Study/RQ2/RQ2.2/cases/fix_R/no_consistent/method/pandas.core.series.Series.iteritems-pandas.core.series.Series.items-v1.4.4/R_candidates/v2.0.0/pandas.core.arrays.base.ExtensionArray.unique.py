    def unique(self: ExtensionArrayT) -> ExtensionArrayT:
        """
        Compute the ExtensionArray of unique values.

        Returns
        -------
        pandas.api.extensions.ExtensionArray
        """
        uniques = unique(self.astype(object))
        return self._from_sequence(uniques, dtype=self.dtype)
