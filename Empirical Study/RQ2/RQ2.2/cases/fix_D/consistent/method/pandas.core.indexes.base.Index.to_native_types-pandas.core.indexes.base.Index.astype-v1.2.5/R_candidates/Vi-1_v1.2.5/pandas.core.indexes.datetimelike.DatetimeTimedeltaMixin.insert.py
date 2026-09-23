    @Appender(DatetimeIndexOpsMixin.insert.__doc__)
    def insert(self, loc, item):
        if isinstance(item, str):
            # TODO: Why are strings special?
            # TODO: Should we attempt _scalar_from_string?
            return self.astype(object).insert(loc, item)

        return DatetimeIndexOpsMixin.insert(self, loc, item)
