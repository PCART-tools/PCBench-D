    @Appender(dtl.DatetimeLikeArrayMixin._validate_fill_value.__doc__)
    def _validate_fill_value(self, fill_value):
        if isna(fill_value):
            fill_value = iNaT
        elif isinstance(fill_value, Period):
            self._check_compatible_with(fill_value)
            fill_value = fill_value.ordinal
        else:
            raise ValueError("'fill_value' should be a Period. "
                             "Got '{got}'.".format(got=fill_value))
        return fill_value
