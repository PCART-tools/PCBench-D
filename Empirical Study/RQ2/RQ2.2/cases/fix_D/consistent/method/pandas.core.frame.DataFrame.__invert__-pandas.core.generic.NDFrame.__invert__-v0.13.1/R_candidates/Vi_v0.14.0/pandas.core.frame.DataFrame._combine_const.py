    def _combine_const(self, other, func, raise_on_error=True):
        if self.empty:
            return self

        new_data = self._data.eval(func=func, other=other, raise_on_error=raise_on_error)
        return self._constructor(new_data)
