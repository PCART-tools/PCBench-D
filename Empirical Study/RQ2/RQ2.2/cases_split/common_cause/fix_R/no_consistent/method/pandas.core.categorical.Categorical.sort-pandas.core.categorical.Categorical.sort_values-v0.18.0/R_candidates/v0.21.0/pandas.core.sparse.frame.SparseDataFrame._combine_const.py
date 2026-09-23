    def _combine_const(self, other, func, errors='raise', try_cast=True):
        return self._apply_columns(lambda x: func(x, other))
