    class RelatedManager(superclass):
        def __init__(self, instance):
            super(RelatedManager, self).__init__()

            self.instance = instance
            self.model = rel.related_model
            self.field = rel.field

            self.core_filters = {self.field.name: instance}

        def __call__(self, **kwargs):
            # We use **kwargs rather than a kwarg argument to enforce the
            # `manager='manager_name'` syntax.
            manager = getattr(self.model, kwargs.pop('manager'))
            manager_class = create_reverse_many_to_one_manager(manager.__class__, rel)
            return manager_class(self.instance)
        do_not_call_in_templates = True

        def get_queryset(self):
            try:
                return self.instance._prefetched_objects_cache[self.field.related_query_name()]
            except (AttributeError, KeyError):
                db = self._db or router.db_for_read(self.model, instance=self.instance)
                empty_strings_as_null = connections[db].features.interprets_empty_strings_as_nulls
                qs = super(RelatedManager, self).get_queryset()
                qs._add_hints(instance=self.instance)
                if self._db:
                    qs = qs.using(self._db)
                qs = qs.filter(**self.core_filters)
                for field in self.field.foreign_related_fields:
                    val = getattr(self.instance, field.attname)
                    if val is None or (val == '' and empty_strings_as_null):
                        return qs.none()
                qs._known_related_objects = {self.field: {self.instance.pk: self.instance}}
                return qs

        def get_prefetch_queryset(self, instances, queryset=None):
            if queryset is None:
                queryset = super(RelatedManager, self).get_queryset()

            queryset._add_hints(instance=instances[0])
            queryset = queryset.using(queryset._db or self._db)

            rel_obj_attr = self.field.get_local_related_value
            instance_attr = self.field.get_foreign_related_value
            instances_dict = {instance_attr(inst): inst for inst in instances}
            query = {'%s__in' % self.field.name: instances}
            queryset = queryset.filter(**query)

            # Since we just bypassed this class' get_queryset(), we must manage
            # the reverse relation manually.
            for rel_obj in queryset:
                instance = instances_dict[rel_obj_attr(rel_obj)]
                setattr(rel_obj, self.field.name, instance)
            cache_name = self.field.related_query_name()
            return queryset, rel_obj_attr, instance_attr, False, cache_name

        def add(self, *objs, **kwargs):
            bulk = kwargs.pop('bulk', True)
            objs = list(objs)
            db = router.db_for_write(self.model, instance=self.instance)

            def check_and_update_obj(obj):
                if not isinstance(obj, self.model):
                    raise TypeError("'%s' instance expected, got %r" % (
                        self.model._meta.object_name, obj,
                    ))
                setattr(obj, self.field.name, self.instance)

            if bulk:
                pks = []
                for obj in objs:
                    check_and_update_obj(obj)
                    if obj._state.adding or obj._state.db != db:
                        raise ValueError(
                            "%r instance isn't saved. Use bulk=False or save "
                            "the object first." % obj
                        )
                    pks.append(obj.pk)
                self.model._base_manager.using(db).filter(pk__in=pks).update(**{
                    self.field.name: self.instance,
                })
            else:
                with transaction.atomic(using=db, savepoint=False):
                    for obj in objs:
                        check_and_update_obj(obj)
                        obj.save()
        add.alters_data = True

        def create(self, **kwargs):
            kwargs[self.field.name] = self.instance
            db = router.db_for_write(self.model, instance=self.instance)
            return super(RelatedManager, self.db_manager(db)).create(**kwargs)
        create.alters_data = True

        def get_or_create(self, **kwargs):
            kwargs[self.field.name] = self.instance
            db = router.db_for_write(self.model, instance=self.instance)
            return super(RelatedManager, self.db_manager(db)).get_or_create(**kwargs)
        get_or_create.alters_data = True

        def update_or_create(self, **kwargs):
            kwargs[self.field.name] = self.instance
            db = router.db_for_write(self.model, instance=self.instance)
            return super(RelatedManager, self.db_manager(db)).update_or_create(**kwargs)
        update_or_create.alters_data = True

        # remove() and clear() are only provided if the ForeignKey can have a value of null.
        if rel.field.null:
            def remove(self, *objs, **kwargs):
                if not objs:
                    return
                bulk = kwargs.pop('bulk', True)
                val = self.field.get_foreign_related_value(self.instance)
                old_ids = set()
                for obj in objs:
                    # Is obj actually part of this descriptor set?
                    if self.field.get_local_related_value(obj) == val:
                        old_ids.add(obj.pk)
                    else:
                        raise self.field.remote_field.model.DoesNotExist(
                            "%r is not related to %r." % (obj, self.instance)
                        )
                self._clear(self.filter(pk__in=old_ids), bulk)
            remove.alters_data = True

            def clear(self, **kwargs):
                bulk = kwargs.pop('bulk', True)
                self._clear(self, bulk)
            clear.alters_data = True

            def _clear(self, queryset, bulk):
                db = router.db_for_write(self.model, instance=self.instance)
                queryset = queryset.using(db)
                if bulk:
                    # `QuerySet.update()` is intrinsically atomic.
                    queryset.update(**{self.field.name: None})
                else:
                    with transaction.atomic(using=db, savepoint=False):
                        for obj in queryset:
                            setattr(obj, self.field.name, None)
                            obj.save(update_fields=[self.field.name])
            _clear.alters_data = True

        def set(self, objs, **kwargs):
            # Force evaluation of `objs` in case it's a queryset whose value
            # could be affected by `manager.clear()`. Refs #19816.
            objs = tuple(objs)

            bulk = kwargs.pop('bulk', True)
            clear = kwargs.pop('clear', False)

            if self.field.null:
                db = router.db_for_write(self.model, instance=self.instance)
                with transaction.atomic(using=db, savepoint=False):
                    if clear:
                        self.clear()
                        self.add(*objs, bulk=bulk)
                    else:
                        old_objs = set(self.using(db).all())
                        new_objs = []
                        for obj in objs:
                            if obj in old_objs:
                                old_objs.remove(obj)
                            else:
                                new_objs.append(obj)

                        self.remove(*old_objs, bulk=bulk)
                        self.add(*new_objs, bulk=bulk)
            else:
                self.add(*objs, bulk=bulk)
        set.alters_data = True
