    def time_extract_sql(self, lookup_type, field_name):
        return "django_time_extract('%s', %s)" % (lookup_type.lower(), field_name)
