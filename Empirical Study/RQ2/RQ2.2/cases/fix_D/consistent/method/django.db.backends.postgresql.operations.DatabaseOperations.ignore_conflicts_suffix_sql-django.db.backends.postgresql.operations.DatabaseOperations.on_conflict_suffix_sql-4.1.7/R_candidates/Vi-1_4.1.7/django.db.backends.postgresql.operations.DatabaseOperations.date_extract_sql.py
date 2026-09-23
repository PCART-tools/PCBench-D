    def date_extract_sql(self, lookup_type, sql, params):
        # https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT
        extract_sql = f"EXTRACT(%s FROM {sql})"
        extract_param = lookup_type
        if lookup_type == "week_day":
            # For consistency across backends, we return Sunday=1, Saturday=7.
            extract_sql = f"EXTRACT(%s FROM {sql}) + 1"
            extract_param = "dow"
        elif lookup_type == "iso_week_day":
            extract_param = "isodow"
        elif lookup_type == "iso_year":
            extract_param = "isoyear"
        return extract_sql, (extract_param, *params)
