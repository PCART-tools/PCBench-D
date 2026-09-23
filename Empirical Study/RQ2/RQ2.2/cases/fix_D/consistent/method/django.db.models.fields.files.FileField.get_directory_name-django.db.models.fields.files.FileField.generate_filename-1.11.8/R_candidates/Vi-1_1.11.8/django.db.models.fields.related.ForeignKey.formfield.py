    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        if isinstance(self.remote_field.model, six.string_types):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.remote_field.model))
        defaults = {
            'form_class': forms.ModelChoiceField,
            'queryset': self.remote_field.model._default_manager.using(db),
            'to_field_name': self.remote_field.field_name,
        }
        defaults.update(kwargs)
        return super(ForeignKey, self).formfield(**defaults)
