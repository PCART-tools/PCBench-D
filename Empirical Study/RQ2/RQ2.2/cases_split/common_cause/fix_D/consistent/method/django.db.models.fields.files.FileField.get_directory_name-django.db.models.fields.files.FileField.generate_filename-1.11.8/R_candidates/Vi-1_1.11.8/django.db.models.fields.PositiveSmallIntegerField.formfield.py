    def formfield(self, **kwargs):
        defaults = {'min_value': 0}
        defaults.update(kwargs)
        return super(PositiveSmallIntegerField, self).formfield(**defaults)
