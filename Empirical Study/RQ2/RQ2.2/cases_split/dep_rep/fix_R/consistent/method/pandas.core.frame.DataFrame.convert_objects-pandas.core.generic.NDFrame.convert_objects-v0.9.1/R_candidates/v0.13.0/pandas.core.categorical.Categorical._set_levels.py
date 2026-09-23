    def _set_levels(self, levels):
        from pandas.core.index import _ensure_index

        levels = _ensure_index(levels)
        if not levels.is_unique:
            raise ValueError('Categorical levels must be unique')
        self._levels = levels
