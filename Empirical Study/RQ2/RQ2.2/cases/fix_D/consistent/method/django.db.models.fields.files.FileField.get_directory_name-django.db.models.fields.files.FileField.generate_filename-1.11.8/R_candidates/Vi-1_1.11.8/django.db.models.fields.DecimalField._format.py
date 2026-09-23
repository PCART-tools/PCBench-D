    def _format(self, value):
        if isinstance(value, six.string_types):
            return value
        else:
            return self.format_number(value)
