    def date_extract_sql(self, lookup_type, field_name):
        if lookup_type == 'week_day':
            # TO_CHAR(field, 'D') returns an integer from 1-7, where 1=Sunday.
            return "TO_CHAR(%s, 'D')" % field_name
        elif lookup_type == 'week':
            # IW = ISO week number
            return "TO_CHAR(%s, 'IW')" % field_name
        elif lookup_type == 'quarter':
            return "TO_CHAR(%s, 'Q')" % field_name
        else:
            # https://docs.oracle.com/database/121/SQLRF/functions067.htm#SQLRF00639
            return "EXTRACT(%s FROM %s)" % (lookup_type.upper(), field_name)
