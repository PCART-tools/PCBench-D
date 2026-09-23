    def tail(self, n=5):
        """
        Returns last n rows
        """
        l = len(self)
        if abs(n) > l:
            n = l if n > 0 else -l
        return self.iloc[-n:]
