    def _validate_fill_value(self, value):
        # e.g. np.array([1.0]) we want np.array([1], dtype=self.dtype)
        #  see TestSetitemFloatNDarrayIntoIntegerSeries
        super()._validate_fill_value(value)
        if hasattr(value, "dtype") and is_float_dtype(value.dtype):
            converted = value.astype(self.dtype)
            if (converted == value).all():
                # See also: can_hold_element
                return converted
            raise TypeError
        return value
