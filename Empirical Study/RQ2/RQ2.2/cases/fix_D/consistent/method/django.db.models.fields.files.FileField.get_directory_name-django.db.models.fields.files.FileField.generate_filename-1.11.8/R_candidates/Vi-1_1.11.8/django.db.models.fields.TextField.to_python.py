    def to_python(self, value):
        if isinstance(value, six.string_types) or value is None:
            return value
        return force_text(value)
