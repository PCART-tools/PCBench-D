    def get_filename(self, filename):
        warnings.warn(
            'FileField now delegates file name and folder processing to the '
            'storage. get_filename() will be removed in Django 2.0.',
            RemovedInDjango20Warning, stacklevel=2
        )
        return os.path.normpath(self.storage.get_valid_name(os.path.basename(filename)))
