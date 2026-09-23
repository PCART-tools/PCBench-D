    @property
    def _box_func(self):
        return lambda x: tslib.Timedelta(x, unit='ns')
