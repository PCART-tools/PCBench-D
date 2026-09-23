    def _validate_scalar(self, fill_value):
        if fill_value is None:
            # Primarily for subclasses
            fill_value = self.dtype.na_value
        return fill_value
