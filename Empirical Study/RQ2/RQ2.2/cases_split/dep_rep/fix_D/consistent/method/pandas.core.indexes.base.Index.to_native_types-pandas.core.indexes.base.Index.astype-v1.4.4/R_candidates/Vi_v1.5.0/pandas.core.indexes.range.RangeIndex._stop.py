    @property
    def _stop(self) -> int:
        """
        The value of the `stop` parameter.

         .. deprecated:: 0.25.0
            Use ``stop`` instead.
        """
        # GH 25710
        warnings.warn(
            self._deprecation_message.format("_stop", "stop"),
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.stop
