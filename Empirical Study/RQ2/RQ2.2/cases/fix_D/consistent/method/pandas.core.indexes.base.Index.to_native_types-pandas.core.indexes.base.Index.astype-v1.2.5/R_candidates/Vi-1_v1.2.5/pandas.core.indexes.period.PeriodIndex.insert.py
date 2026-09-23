    def insert(self, loc: int, item):
        if not isinstance(item, Period) or self.freq != item.freq:
            return self.astype(object).insert(loc, item)

        return DatetimeIndexOpsMixin.insert(self, loc, item)
