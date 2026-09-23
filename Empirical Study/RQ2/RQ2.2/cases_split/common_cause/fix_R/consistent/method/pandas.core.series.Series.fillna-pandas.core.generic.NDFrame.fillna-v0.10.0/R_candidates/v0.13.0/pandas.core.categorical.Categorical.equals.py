    def equals(self, other):
        """
        Returns True if categorical arrays are equal

        Parameters
        ----------
        other : Categorical

        Returns
        -------
        are_equal : boolean
        """
        if not isinstance(other, Categorical):
            return False

        return (self.levels.equals(other.levels) and
                np.array_equal(self.labels, other.labels))
