    def is_lexsorted(self):
        """
        Return True if the codes are lexicographically sorted
        """
        return self.lexsort_depth == self.nlevels
