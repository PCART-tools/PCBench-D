    def __iter__(self):
        return (self._box_func(v) for v in self.asi8)
