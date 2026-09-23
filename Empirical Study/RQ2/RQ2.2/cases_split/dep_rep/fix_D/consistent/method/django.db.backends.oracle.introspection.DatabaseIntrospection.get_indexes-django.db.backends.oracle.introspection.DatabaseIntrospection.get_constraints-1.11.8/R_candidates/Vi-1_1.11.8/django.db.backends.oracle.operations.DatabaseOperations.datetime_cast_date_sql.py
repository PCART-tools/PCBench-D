    def datetime_cast_date_sql(self, field_name, tzname):
        field_name = self._convert_field_to_tz(field_name, tzname)
        sql = 'TRUNC(%s)' % field_name
        return sql, []
