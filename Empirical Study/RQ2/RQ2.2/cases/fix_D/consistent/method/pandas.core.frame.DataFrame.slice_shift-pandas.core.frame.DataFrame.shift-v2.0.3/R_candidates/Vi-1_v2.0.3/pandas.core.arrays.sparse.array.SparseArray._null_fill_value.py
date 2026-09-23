    @property
    def _null_fill_value(self) -> bool:
        return self._dtype._is_na_fill_value
