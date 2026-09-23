    def insert(self, loc, item):
        if not isinstance(item, Period) or self.freq != item.freq:
            return self.astype(object).insert(loc, item)

        idx = np.concatenate(
            (self[:loc].asi8, np.array([item.ordinal]), self[loc:].asi8)
        )
        return self._shallow_copy(idx)
