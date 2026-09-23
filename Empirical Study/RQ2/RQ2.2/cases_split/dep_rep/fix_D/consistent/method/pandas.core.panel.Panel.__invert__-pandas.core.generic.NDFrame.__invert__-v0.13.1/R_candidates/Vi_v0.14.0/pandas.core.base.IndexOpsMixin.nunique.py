    def nunique(self):
        """
        Return count of unique elements in the object. Excludes NA values.

        Returns
        -------
        nunique : int
        """
        return len(self.value_counts())
