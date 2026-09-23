    def formfield(self, **kwargs):
        defaults = {'form_class': forms.FileField, 'max_length': self.max_length}
        defaults.update(kwargs)
        return super().formfield(**defaults)
