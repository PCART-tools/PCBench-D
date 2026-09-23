class ForwardManyToOneDescriptor(object):
    """
    Accessor to the related object on the forward side of a many-to-one or
    one-to-one relation.

    In the example::

        class Child(Model):
            parent = ForeignKey(Parent, related_name='children')

    ``child.parent`` is a ``ForwardManyToOneDescriptor`` instance.
    """

    def __init__(self, field_with_rel):
        self.field = field_with_rel
        self.cache_name = self.field.get_cache_name()

    @cached_property
    def RelatedObjectDoesNotExist(self):
        # The exception can't be created at initialization time since the
        # related model might not be resolved yet; `rel.model` might still be
        # a string model reference.
        return type(
            str('RelatedObjectDoesNotExist'),
            (self.field.remote_field.model.DoesNotExist, AttributeError),
            {}
        )

    def is_cached(self, instance):
        return hasattr(instance, self.cache_name)

    def get_queryset(self, **hints):
        manager = self.field.remote_field.model._default_manager
        # If the related manager indicates that it should be used for
        # related fields, respect that.
        if not getattr(manager, 'use_for_related_fields', False):
            manager = self.field.remote_field.model._base_manager
        return manager.db_manager(hints=hints).all()

    def get_prefetch_queryset(self, instances, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset._add_hints(instance=instances[0])

        rel_obj_attr = self.field.get_foreign_related_value
        instance_attr = self.field.get_local_related_value
        instances_dict = {instance_attr(inst): inst for inst in instances}
        related_field = self.field.foreign_related_fields[0]

        # FIXME: This will need to be revisited when we introduce support for
        # composite fields. In the meantime we take this practical approach to
        # solve a regression on 1.6 when the reverse manager in hidden
        # (related_name ends with a '+'). Refs #21410.
        # The check for len(...) == 1 is a special case that allows the query
        # to be join-less and smaller. Refs #21760.
        if self.field.remote_field.is_hidden() or len(self.field.foreign_related_fields) == 1:
            query = {'%s__in' % related_field.name: set(instance_attr(inst)[0] for inst in instances)}
        else:
            query = {'%s__in' % self.field.related_query_name(): instances}
        queryset = queryset.filter(**query)

        # Since we're going to assign directly in the cache,
        # we must manage the reverse relation cache manually.
        if not self.field.remote_field.multiple:
            rel_obj_cache_name = self.field.remote_field.get_cache_name()
            for rel_obj in queryset:
                instance = instances_dict[rel_obj_attr(rel_obj)]
                setattr(rel_obj, rel_obj_cache_name, instance)
        return queryset, rel_obj_attr, instance_attr, True, self.cache_name

    def __get__(self, instance, instance_type=None):
        """
        Get the related instance through the forward relation.

        With the example above, when getting ``child.parent``:

        - ``self`` is the descriptor managing the ``parent`` attribute
        - ``instance`` is the ``child`` instance
        - ``instance_type`` in the ``Child`` class (we don't need it)
        """
        if instance is None:
            return self

        # The related instance is loaded from the database and then cached in
        # the attribute defined in self.cache_name. It can also be pre-cached
        # by the reverse accessor (ReverseOneToOneDescriptor).
        try:
            rel_obj = getattr(instance, self.cache_name)
        except AttributeError:
            val = self.field.get_local_related_value(instance)
            if None in val:
                rel_obj = None
            else:
                qs = self.get_queryset(instance=instance)
                qs = qs.filter(**self.field.get_reverse_related_filter(instance))
                # Assuming the database enforces foreign keys, this won't fail.
                rel_obj = qs.get()
                # If this is a one-to-one relation, set the reverse accessor
                # cache on the related object to the current instance to avoid
                # an extra SQL query if it's accessed later on.
                if not self.field.remote_field.multiple:
                    setattr(rel_obj, self.field.remote_field.get_cache_name(), instance)
            setattr(instance, self.cache_name, rel_obj)

        if rel_obj is None and not self.field.null:
            raise self.RelatedObjectDoesNotExist(
                "%s has no %s." % (self.field.model.__name__, self.field.name)
            )
        else:
            return rel_obj

    def __set__(self, instance, value):
        """
        Set the related instance through the forward relation.

        With the example above, when setting ``child.parent = parent``:

        - ``self`` is the descriptor managing the ``parent`` attribute
        - ``instance`` is the ``child`` instance
        - ``value`` in the ``parent`` instance on the right of the equal sign
        """
        # If null=True, we can assign null here, but otherwise the value needs
        # to be an instance of the related class.
        if value is None and self.field.null is False:
            raise ValueError(
                'Cannot assign None: "%s.%s" does not allow null values.' %
                (instance._meta.object_name, self.field.name)
            )
        elif value is not None and not isinstance(value, self.field.remote_field.model):
            raise ValueError(
                'Cannot assign "%r": "%s.%s" must be a "%s" instance.' % (
                    value,
                    instance._meta.object_name,
                    self.field.name,
                    self.field.remote_field.model._meta.object_name,
                )
            )
        elif value is not None:
            if instance._state.db is None:
                instance._state.db = router.db_for_write(instance.__class__, instance=value)
            elif value._state.db is None:
                value._state.db = router.db_for_write(value.__class__, instance=instance)
            elif value._state.db is not None and instance._state.db is not None:
                if not router.allow_relation(value, instance):
                    raise ValueError('Cannot assign "%r": the current database router prevents this relation.' % value)

        # If we're setting the value of a OneToOneField to None, we need to clear
        # out the cache on any old related object. Otherwise, deleting the
        # previously-related object will also cause this object to be deleted,
        # which is wrong.
        if value is None:
            # Look up the previously-related object, which may still be available
            # since we've not yet cleared out the related field.
            # Use the cache directly, instead of the accessor; if we haven't
            # populated the cache, then we don't care - we're only accessing
            # the object to invalidate the accessor cache, so there's no
            # need to populate the cache just to expire it again.
            related = getattr(instance, self.cache_name, None)

            # If we've got an old related object, we need to clear out its
            # cache. This cache also might not exist if the related object
            # hasn't been accessed yet.
            if related is not None:
                setattr(related, self.field.remote_field.get_cache_name(), None)

            for lh_field, rh_field in self.field.related_fields:
                setattr(instance, lh_field.attname, None)

        # Set the values of the related field.
        else:
            for lh_field, rh_field in self.field.related_fields:
                setattr(instance, lh_field.attname, getattr(value, rh_field.attname))

        # Set the related instance cache used by __get__ to avoid a SQL query
        # when accessing the attribute we just set.
        setattr(instance, self.cache_name, value)

        # If this is a one-to-one relation, set the reverse accessor cache on
        # the related object to the current instance to avoid an extra SQL
        # query if it's accessed later on.
        if value is not None and not self.field.remote_field.multiple:
            setattr(value, self.field.remote_field.get_cache_name(), instance)
