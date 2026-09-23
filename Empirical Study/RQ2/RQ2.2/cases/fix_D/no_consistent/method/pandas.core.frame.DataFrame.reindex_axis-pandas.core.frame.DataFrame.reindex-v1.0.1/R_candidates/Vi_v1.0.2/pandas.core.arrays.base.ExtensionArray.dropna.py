    def dropna(self):
        """
        Return ExtensionArray without NA values.

        Returns
        -------
        valid : ExtensionArray
        """
        return self[~self.isna()]
