@total_ordering
@python_2_unicode_compatible
class Field(RegisterLookupMixin):
    """Base class for all field types"""

    # Designates whether empty strings fundamentally are allowed at the
    # database level.
    empty_strings_allowed = True
    empty_values = list(validators.EMPTY_VALUES)

    # These track each time a Field instance is created. Used to retain order.
    # The auto_creation_counter is used for fields that Django implicitly
    # creates, creation_counter is used for all user-specified fields.
    creation_counter = 0
    auto_creation_counter = -1
    default_validators = []  # Default set of validators
    default_error_messages = {
        'invalid_choice': _('Value %(value)r is not a valid choice.'),
        'null': _('This field cannot be null.'),
        'blank': _('This field cannot be blank.'),
        'unique': _('%(model_name)s with this %(field_label)s '
                    'already exists.'),
        # Translators: The 'lookup_type' is one of 'date', 'year' or 'month'.
        # Eg: "Title must be unique for pub_date year"
        'unique_for_date': _("%(field_label)s must be unique for "
                             "%(date_field_label)s %(lookup_type)s."),
    }
    system_check_deprecated_details = None
    system_check_removed_details = None

    # Field flags
    hidden = False

    many_to_many = None
    many_to_one = None
    one_to_many = None
    one_to_one = None
    related_model = None

    # Generic field type description, usually overridden by subclasses
    def _description(self):
        return _('Field of type: %(field_type)s') % {
            'field_type': self.__class__.__name__
        }
    description = property(_description)

    def __init__(self, verbose_name=None, name=None, primary_key=False,
            max_length=None, unique=False, blank=False, null=False,
            db_index=False, rel=None, default=NOT_PROVIDED, editable=True,
            serialize=True, unique_for_date=None, unique_for_month=None,
            unique_for_year=None, choices=None, help_text='', db_column=None,
            db_tablespace=None, auto_created=False, validators=[],
            error_messages=None):
        self.name = name
        self.verbose_name = verbose_name  # May be set by set_attributes_from_name
        self._verbose_name = verbose_name  # Store original for deconstruction
        self.primary_key = primary_key
        self.max_length, self._unique = max_length, unique
        self.blank, self.null = blank, null
        self.remote_field = rel
        self.is_relation = self.remote_field is not None
        self.default = default
        self.editable = editable
        self.serialize = serialize
        self.unique_for_date = unique_for_date
        self.unique_for_month = unique_for_month
        self.unique_for_year = unique_for_year
        if isinstance(choices, collections.Iterator):
            choices = list(choices)
        self.choices = choices or []
        self.help_text = help_text
        self.db_index = db_index
        self.db_column = db_column
        self.db_tablespace = db_tablespace or settings.DEFAULT_INDEX_TABLESPACE
        self.auto_created = auto_created

        # Adjust the appropriate creation counter, and save our local copy.
        if auto_created:
            self.creation_counter = Field.auto_creation_counter
            Field.auto_creation_counter -= 1
        else:
            self.creation_counter = Field.creation_counter
            Field.creation_counter += 1

        self._validators = validators  # Store for deconstruction later

        messages = {}
        for c in reversed(self.__class__.__mro__):
            messages.update(getattr(c, 'default_error_messages', {}))
        messages.update(error_messages or {})
        self._error_messages = error_messages  # Store for deconstruction later
        self.error_messages = messages

    def __str__(self):
        """ Return "app_label.model_label.field_name". """
        model = self.model
        app = model._meta.app_label
        return '%s.%s.%s' % (app, model._meta.object_name, self.name)

    def __repr__(self):
        """
        Displays the module, class and name of the field.
        """
        path = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        name = getattr(self, 'name', None)
        if name is not None:
            return '<%s: %s>' % (path, name)
        return '<%s>' % path

    def check(self, **kwargs):
        errors = []
        errors.extend(self._check_field_name())
        errors.extend(self._check_choices())
        errors.extend(self._check_db_index())
        errors.extend(self._check_null_allowed_for_primary_keys())
        errors.extend(self._check_backend_specific_checks(**kwargs))
        errors.extend(self._check_deprecation_details())
        return errors

    def _check_field_name(self):
        """ Check if field name is valid, i.e. 1) does not end with an
        underscore, 2) does not contain "__" and 3) is not "pk". """

        if self.name.endswith('_'):
            return [
                checks.Error(
                    'Field names must not end with an underscore.',
                    hint=None,
                    obj=self,
                    id='fields.E001',
                )
            ]
        elif '__' in self.name:
            return [
                checks.Error(
                    'Field names must not contain "__".',
                    hint=None,
                    obj=self,
                    id='fields.E002',
                )
            ]
        elif self.name == 'pk':
            return [
                checks.Error(
                    "'pk' is a reserved word that cannot be used as a field name.",
                    hint=None,
                    obj=self,
                    id='fields.E003',
                )
            ]
        else:
            return []

    @property
    def rel(self):
        warnings.warn(
            "Usage of field.rel has been deprecated. Use field.remote_field instead.",
            RemovedInDjango20Warning, 2)
        return self.remote_field

    def _check_choices(self):
        if self.choices:
            if (isinstance(self.choices, six.string_types) or
                    not is_iterable(self.choices)):
                return [
                    checks.Error(
                        "'choices' must be an iterable (e.g., a list or tuple).",
                        hint=None,
                        obj=self,
                        id='fields.E004',
                    )
                ]
            elif any(isinstance(choice, six.string_types) or
                     not is_iterable(choice) or len(choice) != 2
                     for choice in self.choices):
                return [
                    checks.Error(
                        ("'choices' must be an iterable containing "
                         "(actual value, human readable name) tuples."),
                        hint=None,
                        obj=self,
                        id='fields.E005',
                    )
                ]
            else:
                return []
        else:
            return []

    def _check_db_index(self):
        if self.db_index not in (None, True, False):
            return [
                checks.Error(
                    "'db_index' must be None, True or False.",
                    hint=None,
                    obj=self,
                    id='fields.E006',
                )
            ]
        else:
            return []

    def _check_null_allowed_for_primary_keys(self):
        if (self.primary_key and self.null and
                not connection.features.interprets_empty_strings_as_nulls):
            # We cannot reliably check this for backends like Oracle which
            # consider NULL and '' to be equal (and thus set up
            # character-based fields a little differently).
            return [
                checks.Error(
                    'Primary keys must not have null=True.',
                    hint=('Set null=False on the field, or '
                          'remove primary_key=True argument.'),
                    obj=self,
                    id='fields.E007',
                )
            ]
        else:
            return []

    def _check_backend_specific_checks(self, **kwargs):
        app_label = self.model._meta.app_label
        for db in connections:
            if router.allow_migrate(db, app_label, model=self.model):
                return connections[db].validation.check_field(self, **kwargs)
        return []

    def _check_deprecation_details(self):
        if self.system_check_removed_details is not None:
            return [
                checks.Error(
                    self.system_check_removed_details.get(
                        'msg',
                        '%s has been removed except for support in historical '
                        'migrations.' % self.__class__.__name__
                    ),
                    hint=self.system_check_removed_details.get('hint'),
                    obj=self,
                    id=self.system_check_removed_details.get('id', 'fields.EXXX'),
                )
            ]
        elif self.system_check_deprecated_details is not None:
            return [
                checks.Warning(
                    self.system_check_deprecated_details.get(
                        'msg',
                        '%s has been deprecated.' % self.__class__.__name__
                    ),
                    hint=self.system_check_deprecated_details.get('hint'),
                    obj=self,
                    id=self.system_check_deprecated_details.get('id', 'fields.WXXX'),
                )
            ]
        return []

    def get_col(self, alias, output_field=None):
        if output_field is None:
            output_field = self
        if alias != self.model._meta.db_table or output_field != self:
            from django.db.models.expressions import Col
            return Col(alias, self, output_field)
        else:
            return self.cached_col

    @cached_property
    def cached_col(self):
        from django.db.models.expressions import Col
        return Col(self.model._meta.db_table, self)

    def select_format(self, compiler, sql, params):
        """
        Custom format for select clauses. For example, GIS columns need to be
        selected as AsText(table.col) on MySQL as the table.col data can't be used
        by Django.
        """
        return sql, params

    def deconstruct(self):
        """
        Returns enough information to recreate the field as a 4-tuple:

         * The name of the field on the model, if contribute_to_class has been run
         * The import path of the field, including the class: django.db.models.IntegerField
           This should be the most portable version, so less specific may be better.
         * A list of positional arguments
         * A dict of keyword arguments

        Note that the positional or keyword arguments must contain values of the
        following types (including inner values of collection types):

         * None, bool, str, unicode, int, long, float, complex, set, frozenset, list, tuple, dict
         * UUID
         * datetime.datetime (naive), datetime.date
         * top-level classes, top-level functions - will be referenced by their full import path
         * Storage instances - these have their own deconstruct() method

        This is because the values here must be serialized into a text format
        (possibly new Python code, possibly JSON) and these are the only types
        with encoding handlers defined.

        There's no need to return the exact way the field was instantiated this time,
        just ensure that the resulting field is the same - prefer keyword arguments
        over positional ones, and omit parameters with their default values.
        """
        # Short-form way of fetching all the default parameters
        keywords = {}
        possibles = {
            "verbose_name": None,
            "primary_key": False,
            "max_length": None,
            "unique": False,
            "blank": False,
            "null": False,
            "db_index": False,
            "default": NOT_PROVIDED,
            "editable": True,
            "serialize": True,
            "unique_for_date": None,
            "unique_for_month": None,
            "unique_for_year": None,
            "choices": [],
            "help_text": '',
            "db_column": None,
            "db_tablespace": settings.DEFAULT_INDEX_TABLESPACE,
            "auto_created": False,
            "validators": [],
            "error_messages": None,
        }
        attr_overrides = {
            "unique": "_unique",
            "error_messages": "_error_messages",
            "validators": "_validators",
            "verbose_name": "_verbose_name",
        }
        equals_comparison = {"choices", "validators", "db_tablespace"}
        for name, default in possibles.items():
            value = getattr(self, attr_overrides.get(name, name))
            # Unroll anything iterable for choices into a concrete list
            if name == "choices" and isinstance(value, collections.Iterable):
                value = list(value)
            # Do correct kind of comparison
            if name in equals_comparison:
                if value != default:
                    keywords[name] = value
            else:
                if value is not default:
                    keywords[name] = value
        # Work out path - we shorten it for known Django core fields
        path = "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
        if path.startswith("django.db.models.fields.related"):
            path = path.replace("django.db.models.fields.related", "django.db.models")
        if path.startswith("django.db.models.fields.files"):
            path = path.replace("django.db.models.fields.files", "django.db.models")
        if path.startswith("django.db.models.fields.proxy"):
            path = path.replace("django.db.models.fields.proxy", "django.db.models")
        if path.startswith("django.db.models.fields"):
            path = path.replace("django.db.models.fields", "django.db.models")
        # Return basic info - other fields should override this.
        return (
            force_text(self.name, strings_only=True),
            path,
            [],
            keywords,
        )

    def clone(self):
        """
        Uses deconstruct() to clone a new copy of this Field.
        Will not preserve any class attachments/attribute names.
        """
        name, path, args, kwargs = self.deconstruct()
        return self.__class__(*args, **kwargs)

    def __eq__(self, other):
        # Needed for @total_ordering
        if isinstance(other, Field):
            return self.creation_counter == other.creation_counter
        return NotImplemented

    def __lt__(self, other):
        # This is needed because bisect does not take a comparison function.
        if isinstance(other, Field):
            return self.creation_counter < other.creation_counter
        return NotImplemented

    def __hash__(self):
        return hash(self.creation_counter)

    def __deepcopy__(self, memodict):
        # We don't have to deepcopy very much here, since most things are not
        # intended to be altered after initial creation.
        obj = copy.copy(self)
        if self.remote_field:
            obj.remote_field = copy.copy(self.remote_field)
            if hasattr(self.remote_field, 'field') and self.remote_field.field is self:
                obj.remote_field.field = obj
        memodict[id(self)] = obj
        return obj

    def __copy__(self):
        # We need to avoid hitting __reduce__, so define this
        # slightly weird copy construct.
        obj = Empty()
        obj.__class__ = self.__class__
        obj.__dict__ = self.__dict__.copy()
        return obj

    def __reduce__(self):
        """
        Pickling should return the model._meta.fields instance of the field,
        not a new copy of that field. So, we use the app registry to load the
        model and then the field back.
        """
        if not hasattr(self, 'model'):
            # Fields are sometimes used without attaching them to models (for
            # example in aggregation). In this case give back a plain field
            # instance. The code below will create a new empty instance of
            # class self.__class__, then update its dict with self.__dict__
            # values - so, this is very close to normal pickle.
            return _empty, (self.__class__,), self.__dict__
        if self.model._deferred:
            # Deferred model will not be found from the app registry. This
            # could be fixed by reconstructing the deferred model on unpickle.
            raise RuntimeError("Fields of deferred models can't be reduced")
        return _load_field, (self.model._meta.app_label, self.model._meta.object_name,
                             self.name)

    def get_pk_value_on_save(self, instance):
        """
        Hook to generate new PK values on save. This method is called when
        saving instances with no primary key value set. If this method returns
        something else than None, then the returned value is used when saving
        the new instance.
        """
        if self.default:
            return self.get_default()
        return None

    def to_python(self, value):
        """
        Converts the input value into the expected Python data type, raising
        django.core.exceptions.ValidationError if the data can't be converted.
        Returns the converted value. Subclasses should override this.
        """
        return value

    @cached_property
    def validators(self):
        # Some validators can't be created at field initialization time.
        # This method provides a way to delay their creation until required.
        return self.default_validators + self._validators

    def run_validators(self, value):
        if value in self.empty_values:
            return

        errors = []
        for v in self.validators:
            try:
                v(value)
            except exceptions.ValidationError as e:
                if hasattr(e, 'code') and e.code in self.error_messages:
                    e.message = self.error_messages[e.code]
                errors.extend(e.error_list)

        if errors:
            raise exceptions.ValidationError(errors)

    def validate(self, value, model_instance):
        """
        Validates value and throws ValidationError. Subclasses should override
        this to provide validation logic.
        """
        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if self.choices and value not in self.empty_values:
            for option_key, option_value in self.choices:
                if isinstance(option_value, (list, tuple)):
                    # This is an optgroup, so look inside the group for
                    # options.
                    for optgroup_key, optgroup_value in option_value:
                        if value == optgroup_key:
                            return
                elif value == option_key:
                    return
            raise exceptions.ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value},
            )

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'], code='null')

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages['blank'], code='blank')

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python and validate are propagated. The correct value is
        returned if no error is raised.
        """
        value = self.to_python(value)
        self.validate(value, model_instance)
        self.run_validators(value)
        return value

    def db_type(self, connection):
        """
        Returns the database column data type for this field, for the provided
        connection.
        """
        # The default implementation of this method looks at the
        # backend-specific data_types dictionary, looking up the field by its
        # "internal type".
        #
        # A Field class can implement the get_internal_type() method to specify
        # which *preexisting* Django Field class it's most similar to -- i.e.,
        # a custom field might be represented by a TEXT column type, which is
        # the same as the TextField Django field type, which means the custom
        # field's get_internal_type() returns 'TextField'.
        #
        # But the limitation of the get_internal_type() / data_types approach
        # is that it cannot handle database column types that aren't already
        # mapped to one of the built-in Django field types. In this case, you
        # can implement db_type() instead of get_internal_type() to specify
        # exactly which wacky database column type you want to use.
        data = DictWrapper(self.__dict__, connection.ops.quote_name, "qn_")
        try:
            return connection.data_types[self.get_internal_type()] % data
        except KeyError:
            return None

    def db_parameters(self, connection):
        """
        Extension of db_type(), providing a range of different return
        values (type, checks).
        This will look at db_type(), allowing custom model fields to override it.
        """
        data = DictWrapper(self.__dict__, connection.ops.quote_name, "qn_")
        type_string = self.db_type(connection)
        try:
            check_string = connection.data_type_check_constraints[self.get_internal_type()] % data
        except KeyError:
            check_string = None
        return {
            "type": type_string,
            "check": check_string,
        }

    def db_type_suffix(self, connection):
        return connection.data_types_suffix.get(self.get_internal_type())

    def get_db_converters(self, connection):
        if hasattr(self, 'from_db_value'):
            return [self.from_db_value]
        return []

    @property
    def unique(self):
        return self._unique or self.primary_key

    def set_attributes_from_name(self, name):
        if not self.name:
            self.name = name
        self.attname, self.column = self.get_attname_column()
        self.concrete = self.column is not None
        if self.verbose_name is None and self.name:
            self.verbose_name = self.name.replace('_', ' ')

    def contribute_to_class(self, cls, name, virtual_only=False):
        self.set_attributes_from_name(name)
        self.model = cls
        if virtual_only:
            cls._meta.add_field(self, virtual=True)
        else:
            cls._meta.add_field(self)
        if self.choices:
            setattr(cls, 'get_%s_display' % self.name,
                    curry(cls._get_FIELD_display, field=self))

    def get_filter_kwargs_for_object(self, obj):
        """
        Return a dict that when passed as kwargs to self.model.filter(), would
        yield all instances having the same value for this field as obj has.
        """
        return {self.name: getattr(obj, self.attname)}

    def get_attname(self):
        return self.name

    def get_attname_column(self):
        attname = self.get_attname()
        column = self.db_column or attname
        return attname, column

    def get_cache_name(self):
        return '_%s_cache' % self.name

    def get_internal_type(self):
        return self.__class__.__name__

    def pre_save(self, model_instance, add):
        """
        Returns field's value just before saving.
        """
        return getattr(model_instance, self.attname)

    def get_prep_value(self, value):
        """
        Perform preliminary non-db specific value checks and conversions.
        """
        if isinstance(value, Promise):
            value = value._proxy____cast()
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """Returns field's value prepared for interacting with the database
        backend.

        Used by the default implementations of ``get_db_prep_save``and
        `get_db_prep_lookup```
        """
        if not prepared:
            value = self.get_prep_value(value)
        return value

    def get_db_prep_save(self, value, connection):
        """
        Returns field's value prepared for saving into a database.
        """
        return self.get_db_prep_value(value, connection=connection,
                                      prepared=False)

    def get_prep_lookup(self, lookup_type, value):
        """
        Perform preliminary non-db specific lookup checks and conversions
        """
        if hasattr(value, '_prepare'):
            return value._prepare()

        if lookup_type in {
            'iexact', 'contains', 'icontains',
            'startswith', 'istartswith', 'endswith', 'iendswith',
            'isnull', 'search', 'regex', 'iregex',
        }:
            return value
        elif lookup_type in ('exact', 'gt', 'gte', 'lt', 'lte'):
            return self.get_prep_value(value)
        elif lookup_type in ('range', 'in'):
            return [self.get_prep_value(v) for v in value]
        return self.get_prep_value(value)

    def get_db_prep_lookup(self, lookup_type, value, connection,
                           prepared=False):
        """
        Returns field's value prepared for database lookup.
        """
        if not prepared:
            value = self.get_prep_lookup(lookup_type, value)
            prepared = True
        if hasattr(value, 'get_compiler'):
            value = value.get_compiler(connection=connection)
        if hasattr(value, 'as_sql') or hasattr(value, '_as_sql'):
            # If the value has a relabeled_clone method it means the
            # value will be handled later on.
            if hasattr(value, 'relabeled_clone'):
                return value
            if hasattr(value, 'as_sql'):
                sql, params = value.as_sql()
            else:
                sql, params = value._as_sql(connection=connection)
            return QueryWrapper(('(%s)' % sql), params)

        if lookup_type in ('search', 'regex', 'iregex', 'contains',
                           'icontains', 'iexact', 'startswith', 'endswith',
                           'istartswith', 'iendswith'):
            return [value]
        elif lookup_type in ('exact', 'gt', 'gte', 'lt', 'lte'):
            return [self.get_db_prep_value(value, connection=connection,
                                           prepared=prepared)]
        elif lookup_type in ('range', 'in'):
            return [self.get_db_prep_value(v, connection=connection,
                                           prepared=prepared) for v in value]
        elif lookup_type == 'isnull':
            return []
        else:
            return [value]

    def has_default(self):
        """
        Returns a boolean of whether this field has a default value.
        """
        return self.default is not NOT_PROVIDED

    def get_default(self):
        """
        Returns the default value for this field.
        """
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        if (not self.empty_strings_allowed or (self.null and
                   not connection.features.interprets_empty_strings_as_nulls)):
            return None
        return ""

    def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH, limit_choices_to=None):
        """Returns choices with a default blank choices included, for use
        as SelectField choices for this field."""
        blank_defined = False
        choices = list(self.choices) if self.choices else []
        named_groups = choices and isinstance(choices[0][1], (list, tuple))
        if not named_groups:
            for choice, __ in choices:
                if choice in ('', None):
                    blank_defined = True
                    break

        first_choice = (blank_choice if include_blank and
                        not blank_defined else [])
        if self.choices:
            return first_choice + choices
        rel_model = self.remote_field.model
        limit_choices_to = limit_choices_to or self.get_limit_choices_to()
        if hasattr(self.remote_field, 'get_related_field'):
            lst = [(getattr(x, self.remote_field.get_related_field().attname),
                   smart_text(x))
                   for x in rel_model._default_manager.complex_filter(
                       limit_choices_to)]
        else:
            lst = [(x._get_pk_val(), smart_text(x))
                   for x in rel_model._default_manager.complex_filter(
                       limit_choices_to)]
        return first_choice + lst

    def get_choices_default(self):
        return self.get_choices()

    @warn_about_renamed_method(
        'Field', '_get_val_from_obj', 'value_from_object',
        RemovedInDjango20Warning
    )
    def _get_val_from_obj(self, obj):
        if obj is not None:
            return getattr(obj, self.attname)
        else:
            return self.get_default()

    def value_to_string(self, obj):
        """
        Returns a string value of this field from the passed obj.
        This is used by the serialization framework.
        """
        return smart_text(self.value_from_object(obj))

    def _get_flatchoices(self):
        """Flattened version of choices tuple."""
        flat = []
        for choice, value in self.choices:
            if isinstance(value, (list, tuple)):
                flat.extend(value)
            else:
                flat.append((choice, value))
        return flat
    flatchoices = property(_get_flatchoices)

    def save_form_data(self, instance, data):
        setattr(instance, self.name, data)

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        """
        Returns a django.forms.Field instance for this database Field.
        """
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()
        if self.choices:
            # Fields with choices get special treatment.
            include_blank = (self.blank or
                             not (self.has_default() or 'initial' in kwargs))
            defaults['choices'] = self.get_choices(include_blank=include_blank)
            defaults['coerce'] = self.to_python
            if self.null:
                defaults['empty_value'] = None
            if choices_form_class is not None:
                form_class = choices_form_class
            else:
                form_class = forms.TypedChoiceField
            # Many of the subclass-specific formfield arguments (min_value,
            # max_value) don't apply for choice fields, so be sure to only pass
            # the values that TypedChoiceField will understand.
            for k in list(kwargs):
                if k not in ('coerce', 'empty_value', 'choices', 'required',
                             'widget', 'label', 'initial', 'help_text',
                             'error_messages', 'show_hidden_initial'):
                    del kwargs[k]
        defaults.update(kwargs)
        if form_class is None:
            form_class = forms.CharField
        return form_class(**defaults)

    def value_from_object(self, obj):
        """
        Returns the value of this field in the given model instance.
        """
        return getattr(obj, self.attname)
