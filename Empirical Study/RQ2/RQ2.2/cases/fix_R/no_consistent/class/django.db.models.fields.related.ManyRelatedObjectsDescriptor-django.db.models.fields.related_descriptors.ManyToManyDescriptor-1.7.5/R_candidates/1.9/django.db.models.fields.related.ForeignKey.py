class ForeignKey(ForeignObject):
    """
    Provide a many-to-one relation by adding a column to the local model
    to hold the remote value.

    By default ForeignKey will target the pk of the remote model but this
    behavior can be changed by using the ``to_field`` argument.
    """

    # Field flags
    many_to_many = False
    many_to_one = True
    one_to_many = False
    one_to_one = False

    rel_class = ManyToOneRel

    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _('%(model)s instance with %(field)s %(value)r does not exist.')
    }
    description = _("Foreign Key (type determined by related field)")

    def __init__(self, to, on_delete=None, related_name=None, related_query_name=None,
            limit_choices_to=None, parent_link=False, to_field=None,
            db_constraint=True, **kwargs):
        try:
            to._meta.model_name
        except AttributeError:
            assert isinstance(to, six.string_types), (
                "%s(%r) is invalid. First parameter to ForeignKey must be "
                "either a model, a model name, or the string %r" % (
                    self.__class__.__name__, to,
                    RECURSIVE_RELATIONSHIP_CONSTANT,
                )
            )
        else:
            # For backwards compatibility purposes, we need to *try* and set
            # the to_field during FK construction. It won't be guaranteed to
            # be correct until contribute_to_class is called. Refs #12190.
            to_field = to_field or (to._meta.pk and to._meta.pk.name)

        if on_delete is None:
            warnings.warn(
                "on_delete will be a required arg for %s in Django 2.0. "
                "Set it to models.CASCADE if you want to maintain the current default behavior. "
                "See https://docs.djangoproject.com/en/%s/ref/models/fields/"
                "#django.db.models.ForeignKey.on_delete" % (
                    self.__class__.__name__,
                    get_docs_version(),
                ),
                RemovedInDjango20Warning, 2)
            on_delete = CASCADE

        elif not callable(on_delete):
            warnings.warn(
                "The signature for {0} will change in Django 2.0. "
                "Pass to_field='{1}' as a kwarg instead of as an arg.".format(
                    self.__class__.__name__,
                    on_delete,
                ),
                RemovedInDjango20Warning, 2)
            on_delete, to_field = to_field, on_delete

        kwargs['rel'] = self.rel_class(
            self, to, to_field,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            on_delete=on_delete,
        )

        kwargs['db_index'] = kwargs.get('db_index', True)

        super(ForeignKey, self).__init__(
            to, on_delete, from_fields=['self'], to_fields=[to_field], **kwargs)

        self.db_constraint = db_constraint

    def check(self, **kwargs):
        errors = super(ForeignKey, self).check(**kwargs)
        errors.extend(self._check_on_delete())
        errors.extend(self._check_unique())
        return errors

    def _check_on_delete(self):
        on_delete = getattr(self.remote_field, 'on_delete', None)
        if on_delete == SET_NULL and not self.null:
            return [
                checks.Error(
                    'Field specifies on_delete=SET_NULL, but cannot be null.',
                    hint='Set null=True argument on the field, or change the on_delete rule.',
                    obj=self,
                    id='fields.E320',
                )
            ]
        elif on_delete == SET_DEFAULT and not self.has_default():
            return [
                checks.Error(
                    'Field specifies on_delete=SET_DEFAULT, but has no default value.',
                    hint='Set a default value, or change the on_delete rule.',
                    obj=self,
                    id='fields.E321',
                )
            ]
        else:
            return []

    def _check_unique(self, **kwargs):
        return [
            checks.Warning(
                'Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.',
                hint='ForeignKey(unique=True) is usually better served by a OneToOneField.',
                obj=self,
                id='fields.W342',
            )
        ] if self.unique else []

    def deconstruct(self):
        name, path, args, kwargs = super(ForeignKey, self).deconstruct()
        del kwargs['to_fields']
        del kwargs['from_fields']
        # Handle the simpler arguments
        if self.db_index:
            del kwargs['db_index']
        else:
            kwargs['db_index'] = False
        if self.db_constraint is not True:
            kwargs['db_constraint'] = self.db_constraint
        # Rel needs more work.
        to_meta = getattr(self.remote_field.model, "_meta", None)
        if self.remote_field.field_name and (
                not to_meta or (to_meta.pk and self.remote_field.field_name != to_meta.pk.name)):
            kwargs['to_field'] = self.remote_field.field_name
        return name, path, args, kwargs

    @property
    def target_field(self):
        return self.foreign_related_fields[0]

    def get_reverse_path_info(self):
        """
        Get path from the related model to this field's model.
        """
        opts = self.model._meta
        from_opts = self.remote_field.model._meta
        pathinfos = [PathInfo(from_opts, opts, (opts.pk,), self.remote_field, not self.unique, False)]
        return pathinfos

    def validate(self, value, model_instance):
        if self.remote_field.parent_link:
            return
        super(ForeignKey, self).validate(value, model_instance)
        if value is None:
            return

        using = router.db_for_read(model_instance.__class__, instance=model_instance)
        qs = self.remote_field.model._default_manager.using(using).filter(
            **{self.remote_field.field_name: value}
        )
        qs = qs.complex_filter(self.get_limit_choices_to())
        if not qs.exists():
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={
                    'model': self.remote_field.model._meta.verbose_name, 'pk': value,
                    'field': self.remote_field.field_name, 'value': value,
                },  # 'pk' is included for backwards compatibility
            )

    def get_attname(self):
        return '%s_id' % self.name

    def get_attname_column(self):
        attname = self.get_attname()
        column = self.db_column or attname
        return attname, column

    def get_default(self):
        "Here we check if the default value is an object and return the to_field if so."
        field_default = super(ForeignKey, self).get_default()
        if isinstance(field_default, self.remote_field.model):
            return getattr(field_default, self.target_field.attname)
        return field_default

    def get_db_prep_save(self, value, connection):
        if value is None or (value == '' and
                             (not self.target_field.empty_strings_allowed or
                              connection.features.interprets_empty_strings_as_nulls)):
            return None
        else:
            return self.target_field.get_db_prep_save(value, connection=connection)

    def get_db_prep_value(self, value, connection, prepared=False):
        return self.target_field.get_db_prep_value(value, connection, prepared)

    def value_to_string(self, obj):
        if not obj:
            # In required many-to-one fields with only one available choice,
            # select that one available choice. Note: For SelectFields
            # we have to check that the length of choices is *2*, not 1,
            # because SelectFields always have an initial "blank" value.
            if not self.blank and self.choices:
                choice_list = self.get_choices_default()
                if len(choice_list) == 2:
                    return smart_text(choice_list[1][0])
        return super(ForeignKey, self).value_to_string(obj)

    def contribute_to_related_class(self, cls, related):
        super(ForeignKey, self).contribute_to_related_class(cls, related)
        if self.remote_field.field_name is None:
            self.remote_field.field_name = cls._meta.pk.name

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        if isinstance(self.remote_field.model, six.string_types):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.remote_field.model))
        defaults = {
            'form_class': forms.ModelChoiceField,
            'queryset': self.remote_field.model._default_manager.using(db),
            'to_field_name': self.remote_field.field_name,
        }
        defaults.update(kwargs)
        return super(ForeignKey, self).formfield(**defaults)

    def db_type(self, connection):
        # The database column type of a ForeignKey is the column type
        # of the field to which it points. An exception is if the ForeignKey
        # points to an AutoField/PositiveIntegerField/PositiveSmallIntegerField,
        # in which case the column type is simply that of an IntegerField.
        # If the database needs similar types for key fields however, the only
        # thing we can do is making AutoField an IntegerField.
        rel_field = self.target_field
        if (isinstance(rel_field, AutoField) or
                (not connection.features.related_fields_match_type and
                isinstance(rel_field, (PositiveIntegerField,
                                       PositiveSmallIntegerField)))):
            return IntegerField().db_type(connection=connection)
        return rel_field.db_type(connection=connection)

    def db_parameters(self, connection):
        return {"type": self.db_type(connection), "check": []}

    def convert_empty_strings(self, value, expression, connection, context):
        if (not value) and isinstance(value, six.string_types):
            return None
        return value

    def get_db_converters(self, connection):
        converters = super(ForeignKey, self).get_db_converters(connection)
        if connection.features.interprets_empty_strings_as_nulls:
            converters += [self.convert_empty_strings]
        return converters

    def get_col(self, alias, output_field=None):
        return super(ForeignKey, self).get_col(alias, output_field or self.target_field)
