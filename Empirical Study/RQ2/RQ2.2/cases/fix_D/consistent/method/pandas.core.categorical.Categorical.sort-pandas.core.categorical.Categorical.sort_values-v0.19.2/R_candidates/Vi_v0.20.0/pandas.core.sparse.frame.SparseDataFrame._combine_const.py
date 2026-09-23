    def _combine_const(self, other, func, raise_on_error=True):
        return self._apply_columns(lambda x: func(x, other))
