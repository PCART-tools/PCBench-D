    def formfield(self, **kwargs):
        defaults = {'min_value': -BigIntegerField.MAX_BIGINT - 1,
                    'max_value': BigIntegerField.MAX_BIGINT}
        defaults.update(kwargs)
        return super(BigIntegerField, self).formfield(**defaults)
