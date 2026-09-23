    def formfield(self, **kwargs):
        defaults = {'form_class': forms.NullBooleanField}
        defaults.update(kwargs)
        return super(NullBooleanField, self).formfield(**defaults)
