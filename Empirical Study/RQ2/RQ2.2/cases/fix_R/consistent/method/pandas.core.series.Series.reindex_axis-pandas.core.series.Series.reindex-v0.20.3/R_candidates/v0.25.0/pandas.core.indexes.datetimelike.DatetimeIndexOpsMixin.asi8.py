    @property  # type: ignore # https://github.com/python/mypy/issues/1362
    @Appender(DatetimeLikeArrayMixin.asi8.__doc__)
    def asi8(self):
        return self._data.asi8
