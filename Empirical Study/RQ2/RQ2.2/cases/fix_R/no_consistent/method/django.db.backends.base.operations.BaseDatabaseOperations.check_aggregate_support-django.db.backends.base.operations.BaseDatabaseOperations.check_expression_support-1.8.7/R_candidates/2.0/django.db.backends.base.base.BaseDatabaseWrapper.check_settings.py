    def check_settings(self):
        if self.settings_dict['TIME_ZONE'] is not None:
            if not settings.USE_TZ:
                raise ImproperlyConfigured(
                    "Connection '%s' cannot set TIME_ZONE because USE_TZ is "
                    "False." % self.alias)
            elif self.features.supports_timezones:
                raise ImproperlyConfigured(
                    "Connection '%s' cannot set TIME_ZONE because its engine "
                    "handles time zones conversions natively." % self.alias)
