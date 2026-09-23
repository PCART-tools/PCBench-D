    def last_valid_index(self):
        """
        Return label for last non-NA/null value
        """
        return self.index[self.count(1) > 0][-1]
