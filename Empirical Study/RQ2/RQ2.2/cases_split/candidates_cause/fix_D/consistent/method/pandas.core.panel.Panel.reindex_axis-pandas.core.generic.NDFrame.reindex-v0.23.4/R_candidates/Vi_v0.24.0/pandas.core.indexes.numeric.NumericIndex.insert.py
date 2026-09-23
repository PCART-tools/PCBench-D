    @Appender(Index.insert.__doc__)
    def insert(self, loc, item):
        # treat NA values as nans:
        if is_scalar(item) and isna(item):
            item = self._na_value
        return super(NumericIndex, self).insert(loc, item)
