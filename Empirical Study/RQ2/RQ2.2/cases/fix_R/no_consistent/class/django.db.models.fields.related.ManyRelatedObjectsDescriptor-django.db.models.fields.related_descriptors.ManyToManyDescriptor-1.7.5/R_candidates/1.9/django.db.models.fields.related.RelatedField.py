class RelatedField(Field):
    """
    Base class that all relational fields inherit from.
    """

    # Field flags
    one_to_many = False
    one_to_one = False
    many_to_many = False
    many_to_one = False

    @cached_property
    def related_model(self):
        # Can't cache this property until all the models are loaded.
        apps.check_models_ready()
        return self.remote_field.model

    def check(self, **kwargs):
        errors = super(RelatedField, self).check(**kwargs)
        errors.extend(self._check_related_name_is_valid())
        errors.extend(self._check_relation_model_exists())
        errors.extend(self._check_referencing_to_swapped_model())
        errors.extend(self._check_clashes())
        return errors

    def _check_related_name_is_valid(self):
        import re
        import keyword
        related_name = self.remote_field.related_name
        if related_name is None:
            return []
        is_valid_id = True
        if keyword.iskeyword(related_name):
            is_valid_id = False
        if six.PY3:
            if not related_name.isidentifier():
                is_valid_id = False
        else:
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\Z', related_name):
                is_valid_id = False
        if not (is_valid_id or related_name.endswith('+')):
            return [
                checks.Error(
                    "The name '%s' is invalid related_name for field %s.%s" %
                    (self.remote_field.related_name, self.model._meta.object_name,
                     self.name),
                    hint="Related name must be a valid Python identifier or end with a '+'",
                    obj=self,
                    id='fields.E306',
                )
            ]
        return []

    def _check_relation_model_exists(self):
        rel_is_missing = self.remote_field.model not in self.opts.apps.get_models()
        rel_is_string = isinstance(self.remote_field.model, six.string_types)
        model_name = self.remote_field.model if rel_is_string else self.remote_field.model._meta.object_name
        if rel_is_missing and (rel_is_string or not self.remote_field.model._meta.swapped):
            return [
                checks.Error(
                    ("Field defines a relation with model '%s', which "
                     "is either not installed, or is abstract.") % model_name,
                    hint=None,
                    obj=self,
                    id='fields.E300',
                )
            ]
        return []

    def _check_referencing_to_swapped_model(self):
        if (self.remote_field.model not in self.opts.apps.get_models() and
                not isinstance(self.remote_field.model, six.string_types) and
                self.remote_field.model._meta.swapped):
            model = "%s.%s" % (
                self.remote_field.model._meta.app_label,
                self.remote_field.model._meta.object_name
            )
            return [
                checks.Error(
                    ("Field defines a relation with the model '%s', "
                     "which has been swapped out.") % model,
                    hint="Update the relation to point at 'settings.%s'." % self.remote_field.model._meta.swappable,
                    obj=self,
                    id='fields.E301',
                )
            ]
        return []

    def _check_clashes(self):
        """
        Check accessor and reverse query name clashes.
        """
        from django.db.models.base import ModelBase

        errors = []
        opts = self.model._meta

        # `f.remote_field.model` may be a string instead of a model. Skip if model name is
        # not resolved.
        if not isinstance(self.remote_field.model, ModelBase):
            return []

        # If the field doesn't install backward relation on the target model (so
        # `is_hidden` returns True), then there are no clashes to check and we
        # can skip these fields.
        if self.remote_field.is_hidden():
            return []

        # Consider that we are checking field `Model.foreign` and the models
        # are:
        #
        #     class Target(models.Model):
        #         model = models.IntegerField()
        #         model_set = models.IntegerField()
        #
        #     class Model(models.Model):
        #         foreign = models.ForeignKey(Target)
        #         m2m = models.ManyToManyField(Target)

        rel_opts = self.remote_field.model._meta
        # rel_opts.object_name == "Target"
        rel_name = self.remote_field.get_accessor_name()  # i. e. "model_set"
        rel_query_name = self.related_query_name()  # i. e. "model"
        field_name = "%s.%s" % (opts.object_name,
            self.name)  # i. e. "Model.field"

        # Check clashes between accessor or reverse query name of `field`
        # and any other field name -- i.e. accessor for Model.foreign is
        # model_set and it clashes with Target.model_set.
        potential_clashes = rel_opts.fields + rel_opts.many_to_many
        for clash_field in potential_clashes:
            clash_name = "%s.%s" % (rel_opts.object_name,
                clash_field.name)  # i. e. "Target.model_set"
            if clash_field.name == rel_name:
                errors.append(
                    checks.Error(
                        "Reverse accessor for '%s' clashes with field name '%s'." % (field_name, clash_name),
                        hint=("Rename field '%s', or add/change a related_name "
                              "argument to the definition for field '%s'.") % (clash_name, field_name),
                        obj=self,
                        id='fields.E302',
                    )
                )

            if clash_field.name == rel_query_name:
                errors.append(
                    checks.Error(
                        "Reverse query name for '%s' clashes with field name '%s'." % (field_name, clash_name),
                        hint=("Rename field '%s', or add/change a related_name "
                              "argument to the definition for field '%s'.") % (clash_name, field_name),
                        obj=self,
                        id='fields.E303',
                    )
                )

        # Check clashes between accessors/reverse query names of `field` and
        # any other field accessor -- i. e. Model.foreign accessor clashes with
        # Model.m2m accessor.
        potential_clashes = (r for r in rel_opts.related_objects if r.field is not self)
        for clash_field in potential_clashes:
            clash_name = "%s.%s" % (  # i. e. "Model.m2m"
                clash_field.related_model._meta.object_name,
                clash_field.field.name)
            if clash_field.get_accessor_name() == rel_name:
                errors.append(
                    checks.Error(
                        "Reverse accessor for '%s' clashes with reverse accessor for '%s'." % (field_name, clash_name),
                        hint=("Add or change a related_name argument "
                              "to the definition for '%s' or '%s'.") % (field_name, clash_name),
                        obj=self,
                        id='fields.E304',
                    )
                )

            if clash_field.get_accessor_name() == rel_query_name:
                errors.append(
                    checks.Error(
                        "Reverse query name for '%s' clashes with reverse query name for '%s'."
                        % (field_name, clash_name),
                        hint=("Add or change a related_name argument "
                              "to the definition for '%s' or '%s'.") % (field_name, clash_name),
                        obj=self,
                        id='fields.E305',
                    )
                )

        return errors

    def db_type(self, connection):
        # By default related field will not have a column as it relates to
        # columns from another table.
        return None

    def contribute_to_class(self, cls, name, virtual_only=False):

        super(RelatedField, self).contribute_to_class(cls, name, virtual_only=virtual_only)

        self.opts = cls._meta

        if not cls._meta.abstract:
            if self.remote_field.related_name:
                related_name = force_text(self.remote_field.related_name) % {
                    'class': cls.__name__.lower(),
                    'app_label': cls._meta.app_label.lower()
                }
                self.remote_field.related_name = related_name

            def resolve_related_class(model, related, field):
                field.remote_field.model = related
                field.do_related_class(related, model)
            lazy_related_operation(resolve_related_class, cls, self.remote_field.model, field=self)

    def get_forward_related_filter(self, obj):
        """
        Return the keyword arguments that when supplied to
        self.model.object.filter(), would select all instances related through
        this field to the remote obj. This is used to build the querysets
        returned by related descriptors. obj is an instance of
        self.related_field.model.
        """
        return {
            '%s__%s' % (self.name, rh_field.name): getattr(obj, rh_field.attname)
            for _, rh_field in self.related_fields
        }

    def get_reverse_related_filter(self, obj):
        """
        Complement to get_forward_related_filter(). Return the keyword
        arguments that when passed to self.related_field.model.object.filter()
        select all instances of self.related_field.model related through
        this field to obj. obj is an instance of self.model.
        """
        base_filter = {
            rh_field.attname: getattr(obj, lh_field.attname)
            for lh_field, rh_field in self.related_fields
        }
        base_filter.update(self.get_extra_descriptor_filter(obj) or {})
        return base_filter

    @property
    def swappable_setting(self):
        """
        Get the setting that this is powered from for swapping, or None
        if it's not swapped in / marked with swappable=False.
        """
        if self.swappable:
            # Work out string form of "to"
            if isinstance(self.remote_field.model, six.string_types):
                to_string = self.remote_field.model
            else:
                to_string = self.remote_field.model._meta.label
            return apps.get_swappable_settings_name(to_string)
        return None

    def set_attributes_from_rel(self):
        self.name = (
            self.name or
            (self.remote_field.model._meta.model_name + '_' + self.remote_field.model._meta.pk.name)
        )
        if self.verbose_name is None:
            self.verbose_name = self.remote_field.model._meta.verbose_name
        self.remote_field.set_field_name()

    @property
    def related(self):
        warnings.warn(
            "Usage of field.related has been deprecated. Use field.remote_field instead.",
            RemovedInDjango110Warning, 2)
        return self.remote_field

    def do_related_class(self, other, cls):
        self.set_attributes_from_rel()
        self.contribute_to_related_class(other, self.remote_field)

    def get_limit_choices_to(self):
        """
        Return ``limit_choices_to`` for this model field.

        If it is a callable, it will be invoked and the result will be
        returned.
        """
        if callable(self.remote_field.limit_choices_to):
            return self.remote_field.limit_choices_to()
        return self.remote_field.limit_choices_to

    def formfield(self, **kwargs):
        """
        Pass ``limit_choices_to`` to the field being constructed.

        Only passes it if there is a type that supports related fields.
        This is a similar strategy used to pass the ``queryset`` to the field
        being constructed.
        """
        defaults = {}
        if hasattr(self.remote_field, 'get_related_field'):
            # If this is a callable, do not invoke it here. Just pass
            # it in the defaults for when the form class will later be
            # instantiated.
            limit_choices_to = self.remote_field.limit_choices_to
            defaults.update({
                'limit_choices_to': limit_choices_to,
            })
        defaults.update(kwargs)
        return super(RelatedField, self).formfield(**defaults)

    def related_query_name(self):
        """
        Define the name that can be used to identify this related object in a
        table-spanning query.
        """
        return self.remote_field.related_query_name or self.remote_field.related_name or self.opts.model_name

    @property
    def target_field(self):
        """
        When filtering against this relation, returns the field on the remote
        model against which the filtering should happen.
        """
        target_fields = self.get_path_info()[-1].target_fields
        if len(target_fields) > 1:
            raise exceptions.FieldError(
                "The relation has multiple target fields, but only single target field was asked for")
        return target_fields[0]
