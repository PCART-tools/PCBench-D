    @property
    def set(self):
        k = len(self.alpha)
        return Interval(0, 1)**k
