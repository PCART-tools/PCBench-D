    def value_from_object(self, obj):
        return [] if obj.pk is None else list(getattr(obj, self.attname).all())
