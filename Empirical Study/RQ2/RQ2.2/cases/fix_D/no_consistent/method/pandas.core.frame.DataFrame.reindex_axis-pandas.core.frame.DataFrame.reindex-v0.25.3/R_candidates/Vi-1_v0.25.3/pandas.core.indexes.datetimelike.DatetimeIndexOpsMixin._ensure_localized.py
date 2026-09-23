    def _ensure_localized(
        self, arg, ambiguous="raise", nonexistent="raise", from_utc=False
    ):
        # See DatetimeLikeArrayMixin._ensure_localized.__doc__
        if getattr(self, "tz", None):
            # ensure_localized is only relevant for tz-aware DTI
            result = self._data._ensure_localized(
                arg, ambiguous=ambiguous, nonexistent=nonexistent, from_utc=from_utc
            )
            return type(self)._simple_new(result, name=self.name)
        return arg
