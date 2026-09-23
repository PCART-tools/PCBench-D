class PositiveIntegerField(IntegerField):
    description = _("Positive integer")

    def get_internal_type(self):
        return "PositiveIntegerField"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0}
        defaults.update(kwargs)
        return super(PositiveIntegerField, self).formfield(**defaults)
