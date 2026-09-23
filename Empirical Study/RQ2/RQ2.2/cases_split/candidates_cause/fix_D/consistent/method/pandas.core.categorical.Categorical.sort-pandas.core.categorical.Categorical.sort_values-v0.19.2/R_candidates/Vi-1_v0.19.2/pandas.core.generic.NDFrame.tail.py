    def tail(self, n=5):
        """
        Returns last n rows
        """
        if n == 0:
            return self.iloc[0:0]
        return self.iloc[-n:]
