    @property
    def is_time_series(self):
        return self._subtyp in ['time_series', 'sparse_time_series']
