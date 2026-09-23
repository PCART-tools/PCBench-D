class ReverseOneToOneDescriptor(object):
    """
    Accessor to the related object on the reverse side of a one-to-one
    relation.

    In the example::

        class Restaurant(Model):
            place = OneToOneField(Place, related_name='restaurant')

    ``place.restaurant`` is a ``ReverseOneToOneDescriptor`` instance.
    """

    def __init__(self, related):
        self.related = related
        self.cache_name = related.get_cache_name()

    @cached_property
    def RelatedObjectDoesNotExist(self):
        # The exception isn't created at initialization time for the sake of
        # consistency with `ForwardManyToOneDescriptor`.
        return type(
            str('RelatedObjectDoesNotExist'),
            (self.related.related_model.DoesNotExist, AttributeError),
            {}
        )

    def is_cached(self, instance):
        return hasattr(instance, self.cache_name)

    def get_queryset(self, **hints):
        manager = self.related.related_model._default_manager
        # If the related manager indicates that it should be used for
        # related fields, respect that.
        if not getattr(manager, 'use_for_related_fields', False):
            manager = self.related.related_model._base_manager
        return manager.db_manager(hints=hints).all()

    def get_prefetch_queryset(self, instances, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset._add_hints(instance=instances[0])

        rel_obj_attr = attrgetter(self.related.field.attname)
        instance_attr = lambda obj: obj._get_pk_val()
        instances_dict = {instance_attr(inst): inst for inst in instances}
        query = {'%s__in' % self.related.field.name: instances}
        queryset = queryset.filter(**query)

        # Since we're going to assign directly in the cache,
        # we must manage the reverse relation cache manually.
        rel_obj_cache_name = self.related.field.get_cache_name()
        for rel_obj in queryset:
            instance = instances_dict[rel_obj_attr(rel_obj)]
            setattr(rel_obj, rel_obj_cache_name, instance)
        return queryset, rel_obj_attr, instance_attr, True, self.cache_name

    def __get__(self, instance, instance_type=None):
        """
        Get the related instance through the reverse relation.

        With the example above, when getting ``place.restaurant``:

        - ``self`` is the descriptor managing the ``restaurant`` attribute
        - ``instance`` is the ``place`` instance
        - ``instance_type`` in the ``Place`` class (we don't need it)

        Keep in mind that ``Restaurant`` holds the foreign key to ``Place``.
        """
        if instance is None:
            return self

        # The related instance is loaded from the database and then cached in
        # the attribute defined in self.cache_name. It can also be pre-cached
        # by the forward accessor (ForwardManyToOneDescriptor).
        try:
            rel_obj = getattr(instance, self.cache_name)
        except AttributeError:
            related_pk = instance._get_pk_val()
            if related_pk is None:
                rel_obj = None
            else:
                filter_args = self.related.field.get_forward_related_filter(instance)
                try:
                    rel_obj = self.get_queryset(instance=instance).get(**filter_args)
                except self.related.related_model.DoesNotExist:
                    rel_obj = None
                else:
                    # Set the forward accessor cache on the related object to
                    # the current instance to avoid an extra SQL query if it's
                    # accessed later on.
                    setattr(rel_obj, self.related.field.get_cache_name(), instance)
            setattr(instance, self.cache_name, rel_obj)

        if rel_obj is None:
            raise self.RelatedObjectDoesNotExist(
                "%s has no %s." % (
                    instance.__class__.__name__,
                    self.related.get_accessor_name()
                )
            )
        else:
            return rel_obj

    def __set__(self, instance, value):
        """
        Set the related instance through the reverse relation.

        With the example above, when setting ``place.restaurant = restaurant``:

        - ``self`` is the descriptor managing the ``restaurant`` attribute
        - ``instance`` is the ``place`` instance
        - ``value`` in the ``restaurant`` instance on the right of the equal sign

        Keep in mind that ``Restaurant`` holds the foreign key to ``Place``.
        """
        # The similarity of the code below to the code in
        # ForwardManyToOneDescriptor is annoying, but there's a bunch
        # of small differences that would make a common base class convoluted.

        # If null=True, we can assign null here, but otherwise the value needs
        # to be an instance of the related class.
        if value is None:
            if self.related.field.null:
                # Update the cached related instance (if any) & clear the cache.
                try:
                    rel_obj = getattr(instance, self.cache_name)
                except AttributeError:
                    pass
                else:
                    delattr(instance, self.cache_name)
                    setattr(rel_obj, self.related.field.name, None)
            else:
                raise ValueError(
                    'Cannot assign None: "%s.%s" does not allow null values.' % (
                        instance._meta.object_name,
                        self.related.get_accessor_name(),
                    )
                )
        elif not isinstance(value, self.related.related_model):
            raise ValueError(
                'Cannot assign "%r": "%s.%s" must be a "%s" instance.' % (
                    value,
                    instance._meta.object_name,
                    self.related.get_accessor_name(),
                    self.related.related_model._meta.object_name,
                )
            )
        else:
            if instance._state.db is None:
                instance._state.db = router.db_for_write(instance.__class__, instance=value)
            elif value._state.db is None:
                value._state.db = router.db_for_write(value.__class__, instance=instance)
            elif value._state.db is not None and instance._state.db is not None:
                if not router.allow_relation(value, instance):
                    raise ValueError('Cannot assign "%r": the current database router prevents this relation.' % value)

            related_pk = tuple(getattr(instance, field.attname) for field in self.related.field.foreign_related_fields)
            # Set the value of the related field to the value of the related object's related field
            for index, field in enumerate(self.related.field.local_related_fields):
                setattr(value, field.attname, related_pk[index])

            # Set the related instance cache used by __get__ to avoid a SQL query
            # when accessing the attribute we just set.
            setattr(instance, self.cache_name, value)

            # Set the forward accessor cache on the related object to the current
            # instance to avoid an extra SQL query if it's accessed later on.
            setattr(value, self.related.field.get_cache_name(), instance)
