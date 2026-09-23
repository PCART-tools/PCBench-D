    def formfield(self, **kwargs):
        defaults = {
            'error_messages': {
                'invalid': _('Enter only digits separated by commas.'),
            }
        }
        defaults.update(kwargs)
        return super(CommaSeparatedIntegerField, self).formfield(**defaults)
