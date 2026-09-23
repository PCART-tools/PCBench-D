    def contribute_to_class(self, cls, name, **kwargs):
        assert not cls._meta.auto_field, "A model can't have more than one AutoField."
        super().contribute_to_class(cls, name, **kwargs)
        cls._meta.auto_field = self
