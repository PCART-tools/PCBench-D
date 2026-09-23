    def _set_scale(self, value, **kwargs):
        self._scale = mscale.scale_factory(value, self, **kwargs)
        self._scale.set_default_locators_and_formatters(self)

        self.isDefault_majloc = True
        self.isDefault_minloc = True
        self.isDefault_majfmt = True
        self.isDefault_minfmt = True
