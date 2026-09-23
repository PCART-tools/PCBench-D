    def _fill_value_matches(self, fill_value):
        if self._null_fill_value:
            return isna(fill_value)
        else:
            return self.fill_value == fill_value
