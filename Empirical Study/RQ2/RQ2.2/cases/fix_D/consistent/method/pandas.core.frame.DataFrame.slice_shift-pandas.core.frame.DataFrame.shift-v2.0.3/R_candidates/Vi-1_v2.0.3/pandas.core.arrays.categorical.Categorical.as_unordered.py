    def as_unordered(self) -> Categorical:
        """
        Set the Categorical to be unordered.

        Returns
        -------
        Categorical
            Unordered Categorical.
        """
        return self.set_ordered(False)
