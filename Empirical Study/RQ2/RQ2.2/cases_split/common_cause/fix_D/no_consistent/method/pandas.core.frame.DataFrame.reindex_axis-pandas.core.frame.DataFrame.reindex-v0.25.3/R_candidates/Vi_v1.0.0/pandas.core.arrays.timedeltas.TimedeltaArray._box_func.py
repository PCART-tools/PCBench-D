    @property
    def _box_func(self):
        return lambda x: Timedelta(x, unit="ns")
