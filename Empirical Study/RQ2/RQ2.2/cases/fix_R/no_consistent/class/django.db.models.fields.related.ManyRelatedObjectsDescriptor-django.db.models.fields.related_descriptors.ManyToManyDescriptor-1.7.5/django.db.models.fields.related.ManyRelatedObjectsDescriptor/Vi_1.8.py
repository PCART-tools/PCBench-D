class ManyRelatedObjectsDescriptor(object):
    # This class provides the functionality that makes the related-object
    # managers available as attributes on a model class, for fields that have
    # multiple "remote" values and have a ManyToManyField pointed at them by
    # some other model (rather than having a ManyToManyField themselves).
    # In the example "publication.article_set", the article_set attribute is a
    # ManyRelatedObjectsDescriptor instance.
    def __init__(self, related):
        self.related = related   # RelatedObject instance

    @cached_property
    def related_manager_cls(self):
        # Dynamically create a class that subclasses the related
        # model's default manager.
        return create_many_related_manager(
            self.related.related_model._default_manager.__class__,
            self.related.field.rel
        )

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        rel_model = self.related.related_model

        manager = self.related_manager_cls(
            model=rel_model,
            query_field_name=self.related.field.name,
            prefetch_cache_name=self.related.field.related_query_name(),
            instance=instance,
            symmetrical=False,
            source_field_name=self.related.field.m2m_reverse_field_name(),
            target_field_name=self.related.field.m2m_field_name(),
            reverse=True,
            through=self.related.field.rel.through,
        )

        return manager

    def __set__(self, instance, value):
        if not self.related.field.rel.through._meta.auto_created:
            opts = self.related.field.rel.through._meta
            raise AttributeError(
                "Cannot set values on a ManyToManyField which specifies an "
                "intermediary model. Use %s.%s's Manager instead." % (opts.app_label, opts.object_name)
            )

        # Force evaluation of `value` in case it's a queryset whose
        # value could be affected by `manager.clear()`. Refs #19816.
        value = tuple(value)

        manager = self.__get__(instance)
        db = router.db_for_write(manager.through, instance=manager.instance)
        with transaction.atomic(using=db, savepoint=False):
            manager.clear()
            manager.add(*value)
