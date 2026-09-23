    def get_prep_value(self, value):
        value = super(DateField, self).get_prep_value(value)
        return self.to_python(value)
