    def __getitem__(self, item: int) -> dt.date | dt.datetime | dt.timedelta:
        s = wrap_s(self._s)
        return s[item]
