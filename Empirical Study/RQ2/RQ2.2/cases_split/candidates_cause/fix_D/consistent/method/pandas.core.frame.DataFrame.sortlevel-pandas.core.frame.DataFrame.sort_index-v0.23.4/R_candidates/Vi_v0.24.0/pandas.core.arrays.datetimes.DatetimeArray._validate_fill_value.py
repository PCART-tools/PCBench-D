    @Appender(dtl.DatetimeLikeArrayMixin._validate_fill_value.__doc__)
    def _validate_fill_value(self, fill_value):
        if isna(fill_value):
            fill_value = iNaT
        elif isinstance(fill_value, (datetime, np.datetime64)):
            self._assert_tzawareness_compat(fill_value)
            fill_value = Timestamp(fill_value).value
        else:
            raise ValueError("'fill_value' should be a Timestamp. "
                             "Got '{got}'.".format(got=fill_value))
        return fill_value
