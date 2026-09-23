    @property
    def rel(self):
        warnings.warn(
            "Usage of field.rel has been deprecated. Use field.remote_field instead.",
            RemovedInDjango20Warning, 2)
        return self.remote_field
