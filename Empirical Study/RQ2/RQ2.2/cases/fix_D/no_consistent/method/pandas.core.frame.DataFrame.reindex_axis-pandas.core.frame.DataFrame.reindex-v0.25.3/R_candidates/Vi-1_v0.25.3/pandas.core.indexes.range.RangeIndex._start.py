    @property
    def _start(self):
        """
        The value of the `start` parameter (``0`` if this was not supplied)

         .. deprecated:: 0.25.0
            Use ``start`` instead.
        """
        warnings.warn(
            self._deprecation_message.format("_start", "start"),
            DeprecationWarning,
            stacklevel=2,
        )
        return self.start
