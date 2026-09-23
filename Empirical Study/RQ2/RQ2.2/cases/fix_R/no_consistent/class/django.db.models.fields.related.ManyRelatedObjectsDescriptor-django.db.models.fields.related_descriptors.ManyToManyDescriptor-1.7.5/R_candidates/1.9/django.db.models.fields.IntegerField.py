class IntegerField(Field):
    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _("'%(value)s' value must be an integer."),
    }
    description = _("Integer")

    def check(self, **kwargs):
        errors = super(IntegerField, self).check(**kwargs)
        errors.extend(self._check_max_length_warning())
        return errors

    def _check_max_length_warning(self):
        if self.max_length is not None:
            return [
                checks.Warning(
                    "'max_length' is ignored when used with IntegerField",
                    hint="Remove 'max_length' from field",
                    obj=self,
                    id='fields.W122',
                )
            ]
        return []

    @cached_property
    def validators(self):
        # These validators can't be added at field initialization time since
        # they're based on values retrieved from `connection`.
        range_validators = []
        internal_type = self.get_internal_type()
        min_value, max_value = connection.ops.integer_field_range(internal_type)
        if min_value is not None:
            range_validators.append(validators.MinValueValidator(min_value))
        if max_value is not None:
            range_validators.append(validators.MaxValueValidator(max_value))
        return super(IntegerField, self).validators + range_validators

    def get_prep_value(self, value):
        value = super(IntegerField, self).get_prep_value(value)
        if value is None:
            return None
        return int(value)

    def get_prep_lookup(self, lookup_type, value):
        if ((lookup_type == 'gte' or lookup_type == 'lt')
                and isinstance(value, float)):
            value = math.ceil(value)
        return super(IntegerField, self).get_prep_lookup(lookup_type, value)

    def get_internal_type(self):
        return "IntegerField"

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

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.IntegerField}
        defaults.update(kwargs)
        return super(IntegerField, self).formfield(**defaults)
