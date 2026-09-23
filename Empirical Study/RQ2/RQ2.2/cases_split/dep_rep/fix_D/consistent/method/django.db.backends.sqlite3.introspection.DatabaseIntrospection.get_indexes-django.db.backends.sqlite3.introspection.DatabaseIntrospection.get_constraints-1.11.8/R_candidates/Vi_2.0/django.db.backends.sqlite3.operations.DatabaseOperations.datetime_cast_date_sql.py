    def datetime_cast_date_sql(self, field_name, tzname):
        return "django_datetime_cast_date(%s, %s)" % (
            field_name, self._convert_tzname_to_sql(tzname),
        )
