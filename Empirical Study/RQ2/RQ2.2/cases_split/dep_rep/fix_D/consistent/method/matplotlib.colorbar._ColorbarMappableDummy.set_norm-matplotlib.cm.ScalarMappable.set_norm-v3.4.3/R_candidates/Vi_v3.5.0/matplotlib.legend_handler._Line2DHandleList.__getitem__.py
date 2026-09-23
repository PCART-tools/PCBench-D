    def __getitem__(self, index):
        if index != 0:
            # Make HandlerLine2D return [self._legline] directly after
            # deprecation elapses.
            _api.warn_deprecated(
                "3.5", message="Access to the second element returned by "
                "HandlerLine2D is deprecated since %(since)s; it will be "
                "removed %(removal)s.")
        return [self._legline, self._legline][index]
