    @property
    def _stop(self):
        """
        The value of the `stop` parameter.

         .. deprecated:: 0.25.0
            Use ``stop`` instead.
        """
        # GH 25710
        warnings.warn(
            self._deprecation_message.format("_stop", "stop"),
            FutureWarning,
            stacklevel=2,
        )
        return self.stop
