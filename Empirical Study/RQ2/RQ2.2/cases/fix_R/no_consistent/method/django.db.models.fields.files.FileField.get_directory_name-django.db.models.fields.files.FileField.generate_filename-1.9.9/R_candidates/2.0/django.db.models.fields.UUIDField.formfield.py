    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.UUIDField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
