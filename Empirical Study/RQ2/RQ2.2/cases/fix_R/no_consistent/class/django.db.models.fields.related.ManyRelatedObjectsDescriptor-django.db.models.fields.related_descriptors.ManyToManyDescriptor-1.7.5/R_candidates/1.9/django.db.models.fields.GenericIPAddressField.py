class GenericIPAddressField(Field):
    empty_strings_allowed = False
    description = _("IP address")
    default_error_messages = {}

    def __init__(self, verbose_name=None, name=None, protocol='both',
                 unpack_ipv4=False, *args, **kwargs):
        self.unpack_ipv4 = unpack_ipv4
        self.protocol = protocol
        self.default_validators, invalid_error_message = \
            validators.ip_address_validators(protocol, unpack_ipv4)
        self.default_error_messages['invalid'] = invalid_error_message
        kwargs['max_length'] = 39
        super(GenericIPAddressField, self).__init__(verbose_name, name, *args,
                                                    **kwargs)

    def check(self, **kwargs):
        errors = super(GenericIPAddressField, self).check(**kwargs)
        errors.extend(self._check_blank_and_null_values(**kwargs))
        return errors

    def _check_blank_and_null_values(self, **kwargs):
        if not getattr(self, 'null', False) and getattr(self, 'blank', False):
            return [
                checks.Error(
                    ('GenericIPAddressFields cannot have blank=True if null=False, '
                     'as blank values are stored as nulls.'),
                    hint=None,
                    obj=self,
                    id='fields.E150',
                )
            ]
        return []

    def deconstruct(self):
        name, path, args, kwargs = super(GenericIPAddressField, self).deconstruct()
        if self.unpack_ipv4 is not False:
            kwargs['unpack_ipv4'] = self.unpack_ipv4
        if self.protocol != "both":
            kwargs['protocol'] = self.protocol
        if kwargs.get("max_length") == 39:
            del kwargs['max_length']
        return name, path, args, kwargs

    def get_internal_type(self):
        return "GenericIPAddressField"

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, six.string_types):
            value = force_text(value)
        value = value.strip()
        if ':' in value:
            return clean_ipv6_address(value,
                self.unpack_ipv4, self.error_messages['invalid'])
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return connection.ops.adapt_ipaddressfield_value(value)

    def get_prep_value(self, value):
        value = super(GenericIPAddressField, self).get_prep_value(value)
        if value is None:
            return None
        if value and ':' in value:
            try:
                return clean_ipv6_address(value, self.unpack_ipv4)
            except exceptions.ValidationError:
                pass
        return six.text_type(value)

    def formfield(self, **kwargs):
        defaults = {
            'protocol': self.protocol,
            'form_class': forms.GenericIPAddressField,
        }
        defaults.update(kwargs)
        return super(GenericIPAddressField, self).formfield(**defaults)
