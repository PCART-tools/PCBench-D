    def datetime_extract_sql(self, lookup_type, field_name, tzname):
        return "django_datetime_extract('%s', %s, %s)" % (
            lookup_type.lower(), field_name, self._convert_tzname_to_sql(tzname),
        )
