    def date_interval_sql(self, timedelta):
        return "'%s'" % duration_string(timedelta)
