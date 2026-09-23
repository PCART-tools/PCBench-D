    def take(self, indices, allow_fill=False, fill_value=None):
        from pandas.core.algorithms import take

        result = take(
            self._ndarray, indices, allow_fill=allow_fill, fill_value=fill_value
        )
        return type(self)(result)
