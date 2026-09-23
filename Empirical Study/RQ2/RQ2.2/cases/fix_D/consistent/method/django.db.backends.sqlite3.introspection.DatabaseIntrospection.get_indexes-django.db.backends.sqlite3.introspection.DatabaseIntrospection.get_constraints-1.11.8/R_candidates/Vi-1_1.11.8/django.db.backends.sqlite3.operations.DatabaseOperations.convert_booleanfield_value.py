    def convert_booleanfield_value(self, value, expression, connection, context):
        return bool(value) if value in (1, 0) else value
