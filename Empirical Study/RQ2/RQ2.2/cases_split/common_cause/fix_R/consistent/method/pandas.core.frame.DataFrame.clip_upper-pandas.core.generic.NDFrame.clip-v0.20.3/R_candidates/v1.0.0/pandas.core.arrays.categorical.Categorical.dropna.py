    def dropna(self):
        """
        Return the Categorical without null values.

        Missing values (-1 in .codes) are detected.

        Returns
        -------
        valid : Categorical
        """
        result = self[self.notna()]

        return result
