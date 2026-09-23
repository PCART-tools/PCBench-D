class UUIDField(Field):
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid UUID."),
    }
    description = 'Universally unique identifier'
    empty_strings_allowed = False

    def __init__(self, verbose_name=None, **kwargs):
        kwargs['max_length'] = 32
        super(UUIDField, self).__init__(verbose_name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UUIDField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def get_internal_type(self):
        return "UUIDField"

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)
            except AttributeError:
                raise TypeError(self.error_messages['invalid'] % {'value': value})

        if connection.features.has_native_uuid_field:
            return value
        return value.hex

    def to_python(self, value):
        if value and not isinstance(value, uuid.UUID):
            try:
                return uuid.UUID(value)
            except ValueError:
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.UUIDField,
        }
        defaults.update(kwargs)
        return super(UUIDField, self).formfield(**defaults)
