    def date_extract_sql(self, lookup_type, field_name):
        if lookup_type == 'week_day':
            # TO_CHAR(field, 'D') returns an integer from 1-7, where 1=Sunday.
            return "TO_CHAR(%s, 'D')" % field_name
        elif lookup_type == 'week':
            # IW = ISO week number
            return "TO_CHAR(%s, 'IW')" % field_name
        else:
            # http://docs.oracle.com/cd/B19306_01/server.102/b14200/functions050.htm
            return "EXTRACT(%s FROM %s)" % (lookup_type.upper(), field_name)
