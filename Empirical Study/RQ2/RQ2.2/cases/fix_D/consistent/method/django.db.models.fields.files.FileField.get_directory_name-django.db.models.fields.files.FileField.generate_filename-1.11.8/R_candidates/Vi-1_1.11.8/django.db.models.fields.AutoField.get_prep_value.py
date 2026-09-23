    def get_prep_value(self, value):
        value = super(AutoField, self).get_prep_value(value)
        if value is None:
            return None
        return int(value)
