    def set_params(self, **kwargs):
        """
        Do nothing, and raise a warning. Any locator class not supporting the
        set_params() function will call this.
        """
        _api.warn_external(
            "'set_params()' not defined for locator of type " +
            str(type(self)))
