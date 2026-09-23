    def _set_colorizer_check_keywords(self, colorizer, **kwargs):
        """
        Raises a ValueError if any kwarg is not None while colorizer is not None.
        """
        self._check_exclusionary_keywords(colorizer, **kwargs)
        self.colorizer = colorizer
