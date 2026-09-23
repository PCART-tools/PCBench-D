    def copy(self, deep=False):
        if deep:
            values = self.sp_values.copy()
        else:
            values = self.sp_values

        return self._simple_new(values, self.sp_index, self.dtype)
