    @property
    def is_unique(self):
        """
        Return boolean if values in the object are unique.

        Returns
        -------
        bool
        """
        return self.nunique(dropna=False) == len(self)
