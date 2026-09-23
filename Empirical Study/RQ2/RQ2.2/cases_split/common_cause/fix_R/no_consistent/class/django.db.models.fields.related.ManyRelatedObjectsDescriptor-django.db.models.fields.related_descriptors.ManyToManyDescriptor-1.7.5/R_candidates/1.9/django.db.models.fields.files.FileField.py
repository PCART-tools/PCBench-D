class FileField(Field):

    # The class to wrap instance attributes in. Accessing the file object off
    # the instance will always return an instance of attr_class.
    attr_class = FieldFile

    # The descriptor to use for accessing the attribute off of the class.
    descriptor_class = FileDescriptor

    description = _("File")

    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, **kwargs):
        self._primary_key_set_explicitly = 'primary_key' in kwargs
        self._unique_set_explicitly = 'unique' in kwargs

        self.storage = storage or default_storage
        self.upload_to = upload_to

        kwargs['max_length'] = kwargs.get('max_length', 100)
        super(FileField, self).__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        errors = super(FileField, self).check(**kwargs)
        errors.extend(self._check_unique())
        errors.extend(self._check_primary_key())
        return errors

    def _check_unique(self):
        if self._unique_set_explicitly:
            return [
                checks.Error(
                    "'unique' is not a valid argument for a %s." % self.__class__.__name__,
                    hint=None,
                    obj=self,
                    id='fields.E200',
                )
            ]
        else:
            return []

    def _check_primary_key(self):
        if self._primary_key_set_explicitly:
            return [
                checks.Error(
                    "'primary_key' is not a valid argument for a %s." % self.__class__.__name__,
                    hint=None,
                    obj=self,
                    id='fields.E201',
                )
            ]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super(FileField, self).deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs['upload_to'] = self.upload_to
        if self.storage is not default_storage:
            kwargs['storage'] = self.storage
        return name, path, args, kwargs

    def get_internal_type(self):
        return "FileField"

    def get_prep_lookup(self, lookup_type, value):
        if hasattr(value, 'name'):
            value = value.name
        return super(FileField, self).get_prep_lookup(lookup_type, value)

    def get_prep_value(self, value):
        "Returns field's value prepared for saving into a database."
        value = super(FileField, self).get_prep_value(value)
        # Need to convert File objects provided via a form to unicode for database insertion
        if value is None:
            return None
        return six.text_type(value)

    def pre_save(self, model_instance, add):
        "Returns field's value just before saving."
        file = super(FileField, self).pre_save(model_instance, add)
        if file and not file._committed:
            # Commit the file to storage prior to saving the model
            file.save(file.name, file, save=False)
        return file

    def contribute_to_class(self, cls, name, **kwargs):
        super(FileField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))

    def get_directory_name(self):
        return os.path.normpath(force_text(datetime.datetime.now().strftime(force_str(self.upload_to))))

    def get_filename(self, filename):
        return os.path.normpath(self.storage.get_valid_name(os.path.basename(filename)))

    def generate_filename(self, instance, filename):
        # If upload_to is a callable, make sure that the path it returns is
        # passed through get_valid_name() of the underlying storage.
        if callable(self.upload_to):
            directory_name, filename = os.path.split(self.upload_to(instance, filename))
            filename = self.storage.get_valid_name(filename)
            return os.path.normpath(os.path.join(directory_name, filename))

        return os.path.join(self.get_directory_name(), self.get_filename(filename))

    def save_form_data(self, instance, data):
        # Important: None means "no change", other false value means "clear"
        # This subtle distinction (rather than a more explicit marker) is
        # needed because we need to consume values that are also sane for a
        # regular (non Model-) Form to find in its cleaned_data dictionary.
        if data is not None:
            # This value will be converted to unicode and stored in the
            # database, so leaving False as-is is not acceptable.
            if not data:
                data = ''
            setattr(instance, self.name, data)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.FileField, 'max_length': self.max_length}
        # If a file has been provided previously, then the form doesn't require
        # that a new file is provided this time.
        # The code to mark the form field as not required is used by
        # form_for_instance, but can probably be removed once form_for_instance
        # is gone. ModelForm uses a different method to check for an existing file.
        if 'initial' in kwargs:
            defaults['required'] = False
        defaults.update(kwargs)
        return super(FileField, self).formfield(**defaults)
