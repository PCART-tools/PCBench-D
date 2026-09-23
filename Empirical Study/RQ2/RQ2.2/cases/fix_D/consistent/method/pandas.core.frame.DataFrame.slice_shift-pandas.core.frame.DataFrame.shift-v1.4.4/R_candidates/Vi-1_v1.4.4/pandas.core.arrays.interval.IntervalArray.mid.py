    @property
    def mid(self):
        """
        Return the midpoint of each Interval in the IntervalArray as an Index.
        """
        try:
            return 0.5 * (self.left + self.right)
        except TypeError:
            # datetime safe version
            return self.left + 0.5 * self.length
