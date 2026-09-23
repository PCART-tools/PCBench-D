    def format_ticks(self, values):
        r_mapping = {v: self._text(k) for k, v in self._units.items()}
        return [r_mapping.get(round(val), '') for val in values]
