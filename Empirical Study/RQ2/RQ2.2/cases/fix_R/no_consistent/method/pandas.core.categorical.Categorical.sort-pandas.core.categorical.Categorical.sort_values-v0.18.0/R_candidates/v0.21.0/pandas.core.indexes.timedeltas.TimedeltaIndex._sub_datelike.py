    def _sub_datelike(self, other):
        from pandas import DatetimeIndex
        if other is NaT:
            result = self._nat_new(box=False)
        else:
            raise TypeError("cannot subtract a datelike from a TimedeltaIndex")
        return DatetimeIndex(result, name=self.name, copy=False)
