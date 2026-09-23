    def date_extract_sql(self, lookup_type, field_name):
        if lookup_type == 'week_day':
            # TO_CHAR(field, 'D') returns an integer from 1-7, where 1=Sunday.
            return "TO_CHAR(%s, 'D')" % field_name
        elif lookup_type == 'week':
            # IW = ISO week number
            return "TO_CHAR(%s, 'IW')" % field_name
        elif lookup_type == 'quarter':
            return "TO_CHAR(%s, 'Q')" % field_name
        elif lookup_type == 'iso_year':
            return "TO_CHAR(%s, 'IYYY')" % field_name
        else:
            # https://docs.oracle.com/en/database/oracle/oracle-database/18/sqlrf/EXTRACT-datetime.html
            return "EXTRACT(%s FROM %s)" % (lookup_type.upper(), field_name)
