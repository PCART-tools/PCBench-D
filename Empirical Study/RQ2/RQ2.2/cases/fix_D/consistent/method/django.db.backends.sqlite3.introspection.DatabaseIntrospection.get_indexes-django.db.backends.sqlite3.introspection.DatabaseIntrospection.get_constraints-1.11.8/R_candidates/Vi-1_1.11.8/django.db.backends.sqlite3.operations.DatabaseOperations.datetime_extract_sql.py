    def datetime_extract_sql(self, lookup_type, field_name, tzname):
        # Same comment as in date_extract_sql.
        return "django_datetime_extract('%s', %s, %%s)" % (
            lookup_type.lower(), field_name), [tzname]
