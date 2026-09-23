    @property
    def _is_na_fill_value(self) -> bool:
        from pandas import isna

        return isna(self.fill_value)
