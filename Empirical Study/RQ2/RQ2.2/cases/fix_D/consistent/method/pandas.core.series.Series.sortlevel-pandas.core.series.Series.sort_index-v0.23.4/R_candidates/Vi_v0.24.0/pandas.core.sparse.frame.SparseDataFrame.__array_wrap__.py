    def __array_wrap__(self, result):
        return self._constructor(
            result, index=self.index, columns=self.columns,
            default_kind=self._default_kind,
            default_fill_value=self._default_fill_value).__finalize__(self)
