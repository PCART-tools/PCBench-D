    def __array__(self, dtype=None):
        return com.take_1d(self.levels.values, self.labels)
