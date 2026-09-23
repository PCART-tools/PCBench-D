    def convert_datefield_value(self, value, expression, connection):
        if isinstance(value, Database.Timestamp):
            value = value.date()
        return value
