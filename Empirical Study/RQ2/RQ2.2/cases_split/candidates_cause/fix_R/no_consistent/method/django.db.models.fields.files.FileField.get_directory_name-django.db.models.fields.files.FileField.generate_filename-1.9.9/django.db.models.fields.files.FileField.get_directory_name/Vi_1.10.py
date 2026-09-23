    def get_directory_name(self):
        warnings.warn(
            'FileField now delegates file name and folder processing to the '
            'storage. get_directory_name() will be removed in Django 2.0.',
            RemovedInDjango20Warning, stacklevel=2
        )
        return os.path.normpath(force_text(datetime.datetime.now().strftime(force_str(self.upload_to))))
