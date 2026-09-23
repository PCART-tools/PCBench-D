    def convert_empty_strings(self, value, expression, connection, context):
        if (not value) and isinstance(value, six.string_types):
            return None
        return value
