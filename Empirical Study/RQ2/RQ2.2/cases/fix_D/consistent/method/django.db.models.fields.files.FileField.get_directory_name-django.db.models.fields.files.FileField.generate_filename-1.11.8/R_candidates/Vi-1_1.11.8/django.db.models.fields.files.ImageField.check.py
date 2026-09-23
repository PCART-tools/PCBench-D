    def check(self, **kwargs):
        errors = super(ImageField, self).check(**kwargs)
        errors.extend(self._check_image_library_installed())
        return errors
