    def _combine_const(self, other, func, errors='raise', try_cast=True):
        new_data = self._data.eval(func=func, other=other,
                                   errors=errors,
                                   try_cast=try_cast)
        return self._constructor(new_data)
