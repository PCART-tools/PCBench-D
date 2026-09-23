    def take(self, indices, allow_fill=False, fill_value=None):
        if allow_fill:
            fill_value = self._validate_fill_value(fill_value)

        new_values = take(self.asi8,
                          indices,
                          allow_fill=allow_fill,
                          fill_value=fill_value)

        return type(self)(new_values, dtype=self.dtype)
