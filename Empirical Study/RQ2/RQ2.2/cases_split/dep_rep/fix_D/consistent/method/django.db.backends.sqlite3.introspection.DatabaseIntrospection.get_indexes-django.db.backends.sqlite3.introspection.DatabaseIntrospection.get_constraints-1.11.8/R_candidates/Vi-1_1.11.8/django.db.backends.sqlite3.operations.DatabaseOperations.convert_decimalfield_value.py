    def convert_decimalfield_value(self, value, expression, connection, context):
        if value is not None:
            value = expression.output_field.format_number(value)
            value = backend_utils.typecast_decimal(value)
        return value
