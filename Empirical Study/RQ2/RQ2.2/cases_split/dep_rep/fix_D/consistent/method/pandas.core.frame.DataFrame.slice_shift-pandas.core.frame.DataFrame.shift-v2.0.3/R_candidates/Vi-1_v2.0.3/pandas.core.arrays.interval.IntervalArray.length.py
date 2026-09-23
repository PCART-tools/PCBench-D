    @property
    def length(self) -> Index:
        """
        Return an Index with entries denoting the length of each Interval.
        """
        return self.right - self.left
