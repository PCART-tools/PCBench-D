    def _validate_shift_value(self, fill_value):
        # TODO(2.0): after deprecation in datetimelikearraymixin is enforced,
        #  we can remove this and use validate_fill_value directly
        return self._validate_scalar(fill_value)
