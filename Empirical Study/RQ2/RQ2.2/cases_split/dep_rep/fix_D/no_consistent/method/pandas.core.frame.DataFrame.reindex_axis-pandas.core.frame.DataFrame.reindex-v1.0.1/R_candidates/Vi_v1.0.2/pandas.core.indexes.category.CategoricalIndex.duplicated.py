    @Appender(Index.duplicated.__doc__)
    def duplicated(self, keep="first"):
        codes = self.codes.astype("i8")
        return duplicated_int64(codes, keep)
