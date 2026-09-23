    def get_prep_value(self, value):
        value = super(NullBooleanField, self).get_prep_value(value)
        if value is None:
            return None
        return self.to_python(value)
