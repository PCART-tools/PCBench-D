    def _combine_series_infer(self, other, func, level=None,
                              fill_value=None, try_cast=True):
        if len(other) == 0:
            return self * np.nan

        if len(self) == 0:
            # Ambiguous case, use _series so works with DataFrame
            return self._constructor(data=self._series, index=self.index,
                                     columns=self.columns)

        return self._combine_match_columns(other, func, level=level,
                                           fill_value=fill_value,
                                           try_cast=try_cast)
