    def convert_textfield_value(self, value, expression, connection, context):
        if isinstance(value, Database.LOB):
            value = force_text(value.read())
        return value
