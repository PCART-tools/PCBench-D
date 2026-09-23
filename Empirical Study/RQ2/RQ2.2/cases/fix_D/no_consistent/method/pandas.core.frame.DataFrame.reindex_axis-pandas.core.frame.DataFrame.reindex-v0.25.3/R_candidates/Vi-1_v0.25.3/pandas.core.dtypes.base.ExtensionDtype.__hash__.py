    def __hash__(self):
        return hash(tuple(getattr(self, attr) for attr in self._metadata))
