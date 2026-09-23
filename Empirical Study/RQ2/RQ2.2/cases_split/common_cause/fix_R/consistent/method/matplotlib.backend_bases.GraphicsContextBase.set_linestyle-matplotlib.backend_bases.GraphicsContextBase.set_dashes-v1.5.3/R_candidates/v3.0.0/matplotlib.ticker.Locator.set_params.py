    def set_params(self, **kwargs):
        """
        Do nothing, and rase a warning. Any locator class not supporting the
        set_params() function will call this.
        """
        warnings.warn("'set_params()' not defined for locator of type " +
                      str(type(self)))
