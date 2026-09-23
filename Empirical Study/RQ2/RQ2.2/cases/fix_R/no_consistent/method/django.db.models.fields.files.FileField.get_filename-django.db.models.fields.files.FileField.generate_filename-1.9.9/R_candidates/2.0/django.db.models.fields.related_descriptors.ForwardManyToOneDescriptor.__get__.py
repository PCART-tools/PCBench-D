    def __get__(self, instance, cls=None):
        """
        Get the related instance through the forward relation.

        With the example above, when getting ``child.parent``:

        - ``self`` is the descriptor managing the ``parent`` attribute
        - ``instance`` is the ``child`` instance
        - ``cls`` is the ``Child`` class (we don't need it)
        """
        if instance is None:
            return self

        # The related instance is loaded from the database and then cached
        # by the field on the model instance state. It can also be pre-cached
        # by the reverse accessor (ReverseOneToOneDescriptor).
        try:
            rel_obj = self.field.get_cached_value(instance)
        except KeyError:
            val = self.field.get_local_related_value(instance)
            if None in val:
                rel_obj = None
            else:
                rel_obj = self.get_object(instance)
                remote_field = self.field.remote_field
                # If this is a one-to-one relation, set the reverse accessor
                # cache on the related object to the current instance to avoid
                # an extra SQL query if it's accessed later on.
                if not remote_field.multiple:
                    remote_field.set_cached_value(rel_obj, instance)
            self.field.set_cached_value(instance, rel_obj)

        if rel_obj is None and not self.field.null:
            raise self.RelatedObjectDoesNotExist(
                "%s has no %s." % (self.field.model.__name__, self.field.name)
            )
        else:
            return rel_obj
