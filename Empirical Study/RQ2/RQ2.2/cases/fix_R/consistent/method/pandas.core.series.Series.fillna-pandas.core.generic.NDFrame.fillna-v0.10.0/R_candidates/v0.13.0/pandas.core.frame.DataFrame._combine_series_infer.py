    def _combine_series_infer(self, other, func, fill_value=None):
        if len(other) == 0:
            return self * NA

        if len(self) == 0:
            # Ambiguous case, use _series so works with DataFrame
            return self._constructor(data=self._series, index=self.index,
                                     columns=self.columns)

        # teeny hack because one does DataFrame + TimeSeries all the time
        if self.index.is_all_dates and other.index.is_all_dates:
            warnings.warn(("TimeSeries broadcasting along DataFrame index "
                           "by default is deprecated. Please use "
                           "DataFrame.<op> to explicitly broadcast arithmetic "
                           "operations along the index"),
                          FutureWarning)
            return self._combine_match_index(other, func, fill_value)
        else:
            return self._combine_match_columns(other, func, fill_value)
