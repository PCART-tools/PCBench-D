    def _convert_tzname_to_sql(self, tzname):
        return "'%s'" % tzname if settings.USE_TZ else 'NULL'
