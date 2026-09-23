    def time_trunc_sql(self, lookup_type, field_name):
        return "django_time_trunc('%s', %s)" % (lookup_type.lower(), field_name)
