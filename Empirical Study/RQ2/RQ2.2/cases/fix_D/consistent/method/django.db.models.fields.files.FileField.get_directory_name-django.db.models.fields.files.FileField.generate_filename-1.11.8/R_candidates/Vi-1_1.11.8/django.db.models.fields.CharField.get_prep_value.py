    def get_prep_value(self, value):
        value = super(CharField, self).get_prep_value(value)
        return self.to_python(value)
