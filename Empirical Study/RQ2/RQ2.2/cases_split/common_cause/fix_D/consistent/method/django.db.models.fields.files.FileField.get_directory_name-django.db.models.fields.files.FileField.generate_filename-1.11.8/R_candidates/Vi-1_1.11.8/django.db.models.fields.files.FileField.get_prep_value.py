    def get_prep_value(self, value):
        "Returns field's value prepared for saving into a database."
        value = super(FileField, self).get_prep_value(value)
        # Need to convert File objects provided via a form to unicode for database insertion
        if value is None:
            return None
        return six.text_type(value)
