    def get_field_type(self, data_type, description):
        # If it's a NUMBER with scale == 0, consider it an IntegerField
        if data_type == cx_Oracle.NUMBER:
            precision, scale = description[4:6]
            if scale == 0:
                if precision > 11:
                    return 'BigIntegerField'
                elif precision == 1:
                    return 'BooleanField'
                else:
                    return 'IntegerField'
            elif scale == -127:
                return 'FloatField'

        return super(DatabaseIntrospection, self).get_field_type(data_type, description)
