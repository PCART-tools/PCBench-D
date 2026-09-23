    def fillna(self, value, limit=None, inplace=False, downcast=None):
        # We support filling a DatetimeTZ with a `value` whose timezone
        # is different by coercing to object.
        if self._can_hold_element(value):
            return super().fillna(value, limit, inplace, downcast)

        # different timezones, or a non-tz
        return self.astype(object).fillna(
            value, limit=limit, inplace=inplace, downcast=downcast
        )
