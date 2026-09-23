    @property
    def is_time_series(self):
        warnings.warn("is_time_series is deprecated. Please use "
                      "Series.index.is_all_dates", FutureWarning, stacklevel=2)
        # return self._subtyp in ['time_series', 'sparse_time_series']
        return self.index.is_all_dates
