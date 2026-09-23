    @cached_property
    def timezone(self):
        """
        Time zone for datetimes stored as naive values in the database.

        Return a tzinfo object or None.

        This is only needed when time zone support is enabled and the database
        doesn't support time zones. (When the database supports time zones,
        the adapter handles aware datetimes so Django doesn't need to.)
        """
        if not settings.USE_TZ:
            return None
        elif self.features.supports_timezones:
            return None
        elif self.settings_dict['TIME_ZONE'] is None:
            return timezone.utc
        else:
            return pytz.timezone(self.settings_dict['TIME_ZONE'])
