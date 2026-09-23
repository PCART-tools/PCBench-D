    def datetime_cast_time_sql(self, field_name, tzname):
        return "django_datetime_cast_time(%s, %%s)" % field_name, [tzname]
