    @property
    def _is_na_fill_value(self):
        from pandas.core.dtypes.missing import isna
        return isna(self.fill_value)
