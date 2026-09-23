    def get_db_converters(self, expression):
        converters = super().get_db_converters(expression)
        internal_type = expression.output_field.get_internal_type()
        if internal_type == 'DateTimeField':
            converters.append(self.convert_datetimefield_value)
        elif internal_type == 'DateField':
            converters.append(self.convert_datefield_value)
        elif internal_type == 'TimeField':
            converters.append(self.convert_timefield_value)
        # Converter for Col is added with Database.register_converter()
        # in base.py.
        elif internal_type == 'DecimalField' and not isinstance(expression, Col):
            converters.append(self.convert_decimalfield_value)
        elif internal_type == 'UUIDField':
            converters.append(self.convert_uuidfield_value)
        elif internal_type in ('NullBooleanField', 'BooleanField'):
            converters.append(self.convert_booleanfield_value)
        return converters
