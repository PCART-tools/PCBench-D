    def fillna(self, value, limit=None, inplace=False, downcast=None):
        # We support filling a DatetimeTZ with a `value` whose timezone
        # is different by coercing to object.
        try:
            return super(DatetimeTZBlock, self).fillna(
                value, limit, inplace, downcast
            )
        except (ValueError, TypeError):
            # different timezones, or a non-tz
            return self.astype(object).fillna(
                value, limit=limit, inplace=inplace, downcast=downcast
            )
