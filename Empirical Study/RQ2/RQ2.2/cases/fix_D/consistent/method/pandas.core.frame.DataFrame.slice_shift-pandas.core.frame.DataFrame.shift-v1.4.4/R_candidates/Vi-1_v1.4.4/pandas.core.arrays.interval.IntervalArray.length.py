    @property
    def length(self):
        """
        Return an Index with entries denoting the length of each Interval in
        the IntervalArray.
        """
        return self.right - self.left
