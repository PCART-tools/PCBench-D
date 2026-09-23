    def get_field_type(self, data_type, description):
        if data_type == cx_Oracle.NUMBER:
            precision, scale = description[4:6]
            if scale == 0:
                if precision > 11:
                    return 'BigAutoField' if description.is_autofield else 'BigIntegerField'
                elif precision == 1:
                    return 'BooleanField'
                elif description.is_autofield:
                    return 'AutoField'
                else:
                    return 'IntegerField'
            elif scale == -127:
                return 'FloatField'

        return super().get_field_type(data_type, description)
