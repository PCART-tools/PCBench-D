class CommaSeparatedIntegerField(CharField):
    default_validators = [validators.validate_comma_separated_integer_list]
    description = _("Comma-separated integers")

    def formfield(self, **kwargs):
        defaults = {
            'error_messages': {
                'invalid': _('Enter only digits separated by commas.'),
            }
        }
        defaults.update(kwargs)
        return super(CommaSeparatedIntegerField, self).formfield(**defaults)
