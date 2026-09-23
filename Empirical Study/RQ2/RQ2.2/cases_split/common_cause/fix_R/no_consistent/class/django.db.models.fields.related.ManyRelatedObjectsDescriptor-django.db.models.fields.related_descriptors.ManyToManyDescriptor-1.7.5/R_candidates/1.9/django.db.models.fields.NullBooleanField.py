class NullBooleanField(Field):
    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _("'%(value)s' value must be either None, True or False."),
    }
    description = _("Boolean (Either True, False or None)")

    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super(NullBooleanField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(NullBooleanField, self).deconstruct()
        del kwargs['null']
        del kwargs['blank']
        return name, path, args, kwargs

    def get_internal_type(self):
        return "NullBooleanField"

    def to_python(self, value):
        if value is None:
            return None
        if value in (True, False):
            return bool(value)
        if value in ('None',):
            return None
        if value in ('t', 'True', '1'):
            return True
        if value in ('f', 'False', '0'):
            return False
        raise exceptions.ValidationError(
            self.error_messages['invalid'],
            code='invalid',
            params={'value': value},
        )

    def get_prep_lookup(self, lookup_type, value):
        # Special-case handling for filters coming from a Web request (e.g. the
        # admin interface). Only works for scalar values (not lists). If you're
        # passing in a list, you might as well make things the right type when
        # constructing the list.
        if value in ('1', '0'):
            value = bool(int(value))
        return super(NullBooleanField, self).get_prep_lookup(lookup_type,
                                                             value)

    def get_prep_value(self, value):
        value = super(NullBooleanField, self).get_prep_value(value)
        if value is None:
            return None
        return bool(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.NullBooleanField,
            'required': not self.blank,
            'label': capfirst(self.verbose_name),
            'help_text': self.help_text}
        defaults.update(kwargs)
        return super(NullBooleanField, self).formfield(**defaults)
