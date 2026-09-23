class FilePathField(Field):
    description = _("File path")

    def __init__(self, verbose_name=None, name=None, path='', match=None,
                 recursive=False, allow_files=True, allow_folders=False, **kwargs):
        self.path, self.match, self.recursive = path, match, recursive
        self.allow_files, self.allow_folders = allow_files, allow_folders
        kwargs['max_length'] = kwargs.get('max_length', 100)
        super(FilePathField, self).__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        errors = super(FilePathField, self).check(**kwargs)
        errors.extend(self._check_allowing_files_or_folders(**kwargs))
        return errors

    def _check_allowing_files_or_folders(self, **kwargs):
        if not self.allow_files and not self.allow_folders:
            return [
                checks.Error(
                    "FilePathFields must have either 'allow_files' or 'allow_folders' set to True.",
                    hint=None,
                    obj=self,
                    id='fields.E140',
                )
            ]
        return []

    def deconstruct(self):
        name, path, args, kwargs = super(FilePathField, self).deconstruct()
        if self.path != '':
            kwargs['path'] = self.path
        if self.match is not None:
            kwargs['match'] = self.match
        if self.recursive is not False:
            kwargs['recursive'] = self.recursive
        if self.allow_files is not True:
            kwargs['allow_files'] = self.allow_files
        if self.allow_folders is not False:
            kwargs['allow_folders'] = self.allow_folders
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        return name, path, args, kwargs

    def get_prep_value(self, value):
        value = super(FilePathField, self).get_prep_value(value)
        if value is None:
            return None
        return six.text_type(value)

    def formfield(self, **kwargs):
        defaults = {
            'path': self.path,
            'match': self.match,
            'recursive': self.recursive,
            'form_class': forms.FilePathField,
            'allow_files': self.allow_files,
            'allow_folders': self.allow_folders,
        }
        defaults.update(kwargs)
        return super(FilePathField, self).formfield(**defaults)

    def get_internal_type(self):
        return "FilePathField"
