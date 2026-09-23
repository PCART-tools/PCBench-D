    @Appender(dtl.DatetimeLikeArrayMixin._validate_fill_value.__doc__)
    def _validate_fill_value(self, fill_value):
        if isna(fill_value):
            fill_value = iNaT
        elif isinstance(fill_value, (timedelta, np.timedelta64, Tick)):
            fill_value = Timedelta(fill_value).value
        else:
            raise ValueError(
                "'fill_value' should be a Timedelta. "
                "Got '{got}'.".format(got=fill_value)
            )
        return fill_value
