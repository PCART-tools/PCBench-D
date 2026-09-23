    def inverted(self):
        return LogitTransform(self._nonpositive)
