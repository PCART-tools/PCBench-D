    @Appender(Index.duplicated.__doc__)
    def duplicated(self, keep="first"):
        shape = map(len, self.levels)
        ids = get_group_index(self.codes, shape, sort=False, xnull=False)

        return duplicated_int64(ids, keep)
