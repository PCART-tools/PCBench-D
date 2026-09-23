    def datetime_trunc_sql(self, lookup_type, field_name, tzname):
        # Same comment as in date_trunc_sql.
        return "django_datetime_trunc('%s', %s, %%s)" % (
            lookup_type.lower(), field_name), [tzname]
