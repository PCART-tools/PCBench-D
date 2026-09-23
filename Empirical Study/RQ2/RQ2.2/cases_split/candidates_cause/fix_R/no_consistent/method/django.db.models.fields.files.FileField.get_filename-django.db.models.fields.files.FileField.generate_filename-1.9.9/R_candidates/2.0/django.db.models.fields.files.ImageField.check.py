    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_image_library_installed())
        return errors
