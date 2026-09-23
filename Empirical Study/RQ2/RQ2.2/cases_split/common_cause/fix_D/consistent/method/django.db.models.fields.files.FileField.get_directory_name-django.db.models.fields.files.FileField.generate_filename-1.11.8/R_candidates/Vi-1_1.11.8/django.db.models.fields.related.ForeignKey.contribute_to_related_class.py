    def contribute_to_related_class(self, cls, related):
        super(ForeignKey, self).contribute_to_related_class(cls, related)
        if self.remote_field.field_name is None:
            self.remote_field.field_name = cls._meta.pk.name
