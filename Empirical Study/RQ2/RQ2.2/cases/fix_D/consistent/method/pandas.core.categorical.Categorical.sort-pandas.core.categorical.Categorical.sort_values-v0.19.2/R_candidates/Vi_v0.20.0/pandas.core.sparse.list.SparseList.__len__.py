    def __len__(self):
        return sum(len(c) for c in self._chunks)
