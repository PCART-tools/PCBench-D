    def datetime_trunc_sql(self, lookup_type, field_name, tzname):
        field_name = self._convert_field_to_tz(field_name, tzname)
        # https://docs.oracle.com/database/121/SQLRF/functions271.htm#SQLRF52058
        if lookup_type in ('year', 'month'):
            sql = "TRUNC(%s, '%s')" % (field_name, lookup_type.upper())
        elif lookup_type == 'quarter':
            sql = "TRUNC(%s, 'Q')" % field_name
        elif lookup_type == 'day':
            sql = "TRUNC(%s)" % field_name
        elif lookup_type == 'hour':
            sql = "TRUNC(%s, 'HH24')" % field_name
        elif lookup_type == 'minute':
            sql = "TRUNC(%s, 'MI')" % field_name
        else:
            sql = "CAST(%s AS DATE)" % field_name  # Cast to DATE removes sub-second precision.
        return sql
