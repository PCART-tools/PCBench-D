    def _set_scale(self, value, **kwargs):
        super(ThetaAxis, self)._set_scale(value, **kwargs)
        self._wrap_locator_formatter()
