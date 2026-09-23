    @property
    def set(self):
        return Interval(self.mu - self.s, self.mu + self.s)
