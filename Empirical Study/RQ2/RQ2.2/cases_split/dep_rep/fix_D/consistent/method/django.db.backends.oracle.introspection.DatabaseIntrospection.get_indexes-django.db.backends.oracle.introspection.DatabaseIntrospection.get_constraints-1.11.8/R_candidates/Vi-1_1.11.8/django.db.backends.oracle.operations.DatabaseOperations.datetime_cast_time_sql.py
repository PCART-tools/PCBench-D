    def datetime_cast_time_sql(self, field_name, tzname):
        # Since `TimeField` values are stored as TIMESTAMP where only the date
        # part is ignored, convert the field to the specified timezone.
        field_name = self._convert_field_to_tz(field_name, tzname)
        return field_name, []
