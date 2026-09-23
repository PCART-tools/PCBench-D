    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.DurationField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
