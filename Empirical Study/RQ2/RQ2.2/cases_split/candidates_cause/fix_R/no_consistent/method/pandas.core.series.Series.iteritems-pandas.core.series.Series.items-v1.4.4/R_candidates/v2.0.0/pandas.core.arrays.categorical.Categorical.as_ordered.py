    def as_ordered(self) -> Categorical:
        """
        Set the Categorical to be ordered.

        Returns
        -------
        Categorical
            Ordered Categorical.
        """
        return self.set_ordered(True)
