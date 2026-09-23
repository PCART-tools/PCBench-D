    def tail(self, n=5):
        """
        Returns last n rows
        """
        l = len(self)
        if l == 0 or n == 0:
            return self
        if n > l:
            n = l
        elif n < -l:
            n = -l
        return self.iloc[-n:]
