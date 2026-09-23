    def inverted(self):
        return LogisticTransform(self._nonpositive)
