    def contribute_to_class(self, cls, name, **kwargs):
        super(DateField, self).contribute_to_class(cls, name, **kwargs)
        if not self.null:
            setattr(
                cls, 'get_next_by_%s' % self.name,
                curry(cls._get_next_or_previous_by_FIELD, field=self, is_next=True)
            )
            setattr(
                cls, 'get_previous_by_%s' % self.name,
                curry(cls._get_next_or_previous_by_FIELD, field=self, is_next=False)
            )
