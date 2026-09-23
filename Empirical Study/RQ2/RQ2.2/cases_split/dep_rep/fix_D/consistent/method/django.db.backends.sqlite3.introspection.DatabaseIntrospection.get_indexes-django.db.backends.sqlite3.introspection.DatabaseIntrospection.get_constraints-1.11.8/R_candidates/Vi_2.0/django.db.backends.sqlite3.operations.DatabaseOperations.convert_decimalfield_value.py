    def convert_decimalfield_value(self, value, expression, connection):
        if value is not None:
            value = expression.output_field.format_number(value)
            # Value is not converted to Decimal here as it will be converted
            # later in BaseExpression.convert_value().
        return value
