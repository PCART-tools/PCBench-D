    def date_extract_sql(self, lookup_type, field_name):
        # https://www.postgresql.org/docs/current/static/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT
        if lookup_type == 'week_day':
            # For consistency across backends, we return Sunday=1, Saturday=7.
            return "EXTRACT('dow' FROM %s) + 1" % field_name
        else:
            return "EXTRACT('%s' FROM %s)" % (lookup_type, field_name)
