class AutoField(Field):
    description = _("Integer")

    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _("'%(value)s' value must be an integer."),
    }

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        super(AutoField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super(AutoField, self).check(**kwargs)
        errors.extend(self._check_primary_key())
        return errors

    def _check_primary_key(self):
        if not self.primary_key:
            return [
                checks.Error(
                    'AutoFields must set primary_key=True.',
                    hint=None,
                    obj=self,
                    id='fields.E100',
                ),
            ]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super(AutoField, self).deconstruct()
        del kwargs['blank']
        kwargs['primary_key'] = True
        return name, path, args, kwargs

    def get_internal_type(self):
        return "AutoField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def validate(self, value, model_instance):
        pass

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
            value = connection.ops.validate_autopk_value(value)
        return value

    def get_prep_value(self, value):
        value = super(AutoField, self).get_prep_value(value)
        if value is None:
            return None
        return int(value)

    def contribute_to_class(self, cls, name, **kwargs):
        assert not cls._meta.has_auto_field, \
            "A model can't have more than one AutoField."
        super(AutoField, self).contribute_to_class(cls, name, **kwargs)
        cls._meta.has_auto_field = True
        cls._meta.auto_field = self

    def formfield(self, **kwargs):
        return None
