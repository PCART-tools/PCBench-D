    def containsx(self, x):
        """
        Returns whether `x` is in the closed (:attr:`x0`, :attr:`x1`) interval.
        """
        x0, x1 = self.intervalx
        return x0 <= x <= x1 or x0 >= x >= x1
