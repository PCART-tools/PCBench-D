    @cache_readonly
    def mid(self):
        """Returns the mid-point of each interval in the index as an array
        """
        try:
            return Index(0.5 * (self.left.values + self.right.values))
        except TypeError:
            # datetime safe version
            delta = self.right.values - self.left.values
            return Index(self.left.values + 0.5 * delta)
