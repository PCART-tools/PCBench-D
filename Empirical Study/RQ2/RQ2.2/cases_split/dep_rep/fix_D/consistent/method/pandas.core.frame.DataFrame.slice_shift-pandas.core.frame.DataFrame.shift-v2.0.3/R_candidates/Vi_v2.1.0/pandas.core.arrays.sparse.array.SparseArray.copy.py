    def copy(self) -> Self:
        values = self.sp_values.copy()
        return self._simple_new(values, self.sp_index, self.dtype)
