    def get_prep_value(self, value):
        value = super(FilePathField, self).get_prep_value(value)
        if value is None:
            return None
        return six.text_type(value)
