class IPAddressField(Field):
    empty_strings_allowed = False
    description = _("IPv4 address")
    system_check_removed_details = {
        'msg': (
            'IPAddressField has been removed except for support in '
            'historical migrations.'
        ),
        'hint': 'Use GenericIPAddressField instead.',
        'id': 'fields.E900',
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15
        super(IPAddressField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(IPAddressField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def get_prep_value(self, value):
        value = super(IPAddressField, self).get_prep_value(value)
        if value is None:
            return None
        return six.text_type(value)

    def get_internal_type(self):
        return "IPAddressField"
