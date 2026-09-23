    def convert_timefield_value(self, value, expression, connection, context):
        if isinstance(value, Database.Timestamp):
            value = value.time()
        return value
