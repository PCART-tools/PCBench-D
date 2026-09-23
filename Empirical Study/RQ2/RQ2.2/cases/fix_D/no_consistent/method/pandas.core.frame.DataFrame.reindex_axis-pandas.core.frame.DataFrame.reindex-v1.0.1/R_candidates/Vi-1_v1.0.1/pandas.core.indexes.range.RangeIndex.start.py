    @cache_readonly
    def start(self):
        """
        The value of the `start` parameter (``0`` if this was not supplied).
        """
        # GH 25710
        return self._range.start
