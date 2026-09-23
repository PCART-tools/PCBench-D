    def convert_timefield_value(self, value, expression, connection, context):
        if value is not None:
            if not isinstance(value, datetime.time):
                value = parse_time(value)
        return value
