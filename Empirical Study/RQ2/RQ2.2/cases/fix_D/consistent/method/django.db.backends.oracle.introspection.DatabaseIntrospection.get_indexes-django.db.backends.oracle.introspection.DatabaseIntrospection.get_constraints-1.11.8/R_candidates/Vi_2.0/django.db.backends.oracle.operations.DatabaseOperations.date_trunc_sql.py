    def date_trunc_sql(self, lookup_type, field_name):
        # https://docs.oracle.com/database/121/SQLRF/functions271.htm#SQLRF52058
        if lookup_type in ('year', 'month'):
            return "TRUNC(%s, '%s')" % (field_name, lookup_type.upper())
        elif lookup_type == 'quarter':
            return "TRUNC(%s, 'Q')" % field_name
        else:
            return "TRUNC(%s)" % field_name
