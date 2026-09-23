    def date_trunc_sql(self, lookup_type, field_name):
        # http://docs.oracle.com/cd/B19306_01/server.102/b14200/functions230.htm#i1002084
        if lookup_type in ('year', 'month'):
            return "TRUNC(%s, '%s')" % (field_name, lookup_type.upper())
        else:
            return "TRUNC(%s)" % field_name
