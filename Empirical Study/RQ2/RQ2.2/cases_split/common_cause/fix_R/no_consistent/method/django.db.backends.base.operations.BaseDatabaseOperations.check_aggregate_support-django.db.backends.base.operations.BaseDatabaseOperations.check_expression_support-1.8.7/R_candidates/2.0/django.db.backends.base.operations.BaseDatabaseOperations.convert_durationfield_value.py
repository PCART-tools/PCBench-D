    def convert_durationfield_value(self, value, expression, connection):
        if value is not None:
            value = str(decimal.Decimal(value) / decimal.Decimal(1000000))
            value = parse_duration(value)
        return value
