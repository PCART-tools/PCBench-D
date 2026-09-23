    def generate_filename(self, instance, filename):
        """
        Apply (if callable) or prepend (if a string) upload_to to the filename,
        then delegate further processing of the name to the storage backend.
        Until the storage layer, all file paths are expected to be Unix style
        (with forward slashes).
        """
        if callable(self.upload_to):
            filename = self.upload_to(instance, filename)
        else:
            dirname = force_text(datetime.datetime.now().strftime(force_str(self.upload_to)))
            filename = posixpath.join(dirname, filename)
        return self.storage.generate_filename(filename)
