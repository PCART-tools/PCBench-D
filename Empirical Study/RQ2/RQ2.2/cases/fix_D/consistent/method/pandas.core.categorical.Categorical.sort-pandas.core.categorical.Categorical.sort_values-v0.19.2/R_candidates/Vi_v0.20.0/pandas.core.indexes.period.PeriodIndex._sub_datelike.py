    def _sub_datelike(self, other):
        if other is tslib.NaT:
            new_data = np.empty(len(self), dtype=np.int64)
            new_data.fill(tslib.iNaT)
            return TimedeltaIndex(new_data, name=self.name)
        return NotImplemented
