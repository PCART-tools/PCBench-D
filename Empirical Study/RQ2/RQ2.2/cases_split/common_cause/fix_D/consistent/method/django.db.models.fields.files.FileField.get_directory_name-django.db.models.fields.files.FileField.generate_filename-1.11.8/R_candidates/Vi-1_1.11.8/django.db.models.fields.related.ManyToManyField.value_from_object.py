    def value_from_object(self, obj):
        """
        Return the value of this field in the given model instance.
        """
        if obj.pk is None:
            return self.related_model.objects.none()
        return getattr(obj, self.attname).all()
