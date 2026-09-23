    def nunique(self):
        """
        Return count of unique elements in the Series

        Returns
        -------
        nunique : int
        """
        return len(self.value_counts())
