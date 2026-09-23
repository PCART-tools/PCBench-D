    def head(self, n=5):
        """
        Returns first n rows
        """
        l = len(self)
        if l == 0 or n==0:
            return self
        return self.iloc[:n]
