    def _box_func(self, x) -> Timedelta | NaTType:
        return Timedelta(x, unit="ns")
