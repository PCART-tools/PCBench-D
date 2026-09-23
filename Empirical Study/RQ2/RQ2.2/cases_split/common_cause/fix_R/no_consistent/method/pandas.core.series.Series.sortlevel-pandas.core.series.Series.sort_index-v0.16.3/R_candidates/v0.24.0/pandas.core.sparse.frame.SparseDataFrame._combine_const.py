    def _combine_const(self, other, func):
        return self._apply_columns(lambda x: func(x, other))
