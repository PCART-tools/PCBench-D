    def is_lexsorted_for_tuple(self, tup):
        """
        Return True if we are correctly lexsorted given the passed tuple
        """
        return len(tup) <= self.lexsort_depth
