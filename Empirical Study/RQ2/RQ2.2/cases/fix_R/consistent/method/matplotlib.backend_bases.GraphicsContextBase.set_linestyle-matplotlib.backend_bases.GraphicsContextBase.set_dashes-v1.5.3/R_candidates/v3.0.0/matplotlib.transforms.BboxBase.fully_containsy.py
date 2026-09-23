    def fully_containsy(self, y):
        """
        Returns whether *y* is in the open (:attr:`y0`, :attr:`y1`) interval.
        """
        y0, y1 = self.intervaly
        return y0 < y < y1 or y0 > y > y1
