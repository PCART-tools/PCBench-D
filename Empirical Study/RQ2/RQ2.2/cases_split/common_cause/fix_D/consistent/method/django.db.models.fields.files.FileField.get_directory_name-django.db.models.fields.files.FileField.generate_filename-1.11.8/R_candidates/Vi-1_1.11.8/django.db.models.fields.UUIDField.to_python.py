    def to_python(self, value):
        if value is not None and not isinstance(value, uuid.UUID):
            try:
                return uuid.UUID(value)
            except (AttributeError, ValueError):
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value
