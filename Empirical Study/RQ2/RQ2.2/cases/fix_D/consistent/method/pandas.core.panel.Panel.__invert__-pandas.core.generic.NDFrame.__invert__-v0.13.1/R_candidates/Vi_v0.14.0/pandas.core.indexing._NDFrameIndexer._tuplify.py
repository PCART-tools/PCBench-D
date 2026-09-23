    def _tuplify(self, loc):
        tup = [slice(None, None) for _ in range(self.ndim)]
        tup[0] = loc
        return tuple(tup)
