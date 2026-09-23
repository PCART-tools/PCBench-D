    def _box_func(self, x) -> Period | NaTType:
        return Period._from_ordinal(ordinal=x, freq=self.freq)
