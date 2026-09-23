    def time_trunc_sql(self, lookup_type, field_name):
        return "DATE_TRUNC('%s', %s)::time" % (lookup_type, field_name)
