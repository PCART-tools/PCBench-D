    def formfield(self, **kwargs):
        defaults = {
            'protocol': self.protocol,
            'form_class': forms.GenericIPAddressField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
