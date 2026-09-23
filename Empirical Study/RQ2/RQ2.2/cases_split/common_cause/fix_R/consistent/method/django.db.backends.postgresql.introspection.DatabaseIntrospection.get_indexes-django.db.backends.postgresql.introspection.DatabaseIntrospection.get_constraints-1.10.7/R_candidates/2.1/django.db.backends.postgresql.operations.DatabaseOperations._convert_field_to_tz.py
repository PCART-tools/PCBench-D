    def _convert_field_to_tz(self, field_name, tzname):
        if settings.USE_TZ:
            field_name = "%s AT TIME ZONE '%s'" % (field_name, tzname)
        return field_name
