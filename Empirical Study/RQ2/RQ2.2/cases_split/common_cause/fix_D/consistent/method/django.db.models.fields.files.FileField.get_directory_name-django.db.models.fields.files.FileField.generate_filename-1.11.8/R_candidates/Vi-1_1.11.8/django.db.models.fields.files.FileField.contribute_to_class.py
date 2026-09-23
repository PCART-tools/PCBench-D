    def contribute_to_class(self, cls, name, **kwargs):
        super(FileField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))
