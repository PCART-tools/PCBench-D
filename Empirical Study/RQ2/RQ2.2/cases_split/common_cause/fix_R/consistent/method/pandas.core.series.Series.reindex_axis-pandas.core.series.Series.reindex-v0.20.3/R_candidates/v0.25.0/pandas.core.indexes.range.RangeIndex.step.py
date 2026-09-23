    @cache_readonly
    def step(self):
        """
        The value of the `step` parameter (``1`` if this was not supplied)
        """
        # GH 25710
        return self._range.step
