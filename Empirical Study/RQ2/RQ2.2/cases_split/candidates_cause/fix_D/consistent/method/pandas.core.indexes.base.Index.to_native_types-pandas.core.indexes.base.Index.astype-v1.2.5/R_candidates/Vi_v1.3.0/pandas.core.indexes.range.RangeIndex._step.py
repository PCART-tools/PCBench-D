    @property
    def _step(self) -> int:
        """
        The value of the `step` parameter (``1`` if this was not supplied).

         .. deprecated:: 0.25.0
            Use ``step`` instead.
        """
        # GH 25710
        warnings.warn(
            self._deprecation_message.format("_step", "step"),
            FutureWarning,
            stacklevel=2,
        )
        return self.step
