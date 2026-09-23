    def _join_i8_wrapper(joinf, **kwargs):
        return DatetimeIndexOpsMixin._join_i8_wrapper(
            joinf, dtype='m8[ns]', **kwargs)
