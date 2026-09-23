    def _validate(self):
        super()._validate()

        if not isinstance(self.win_type, str):
            raise ValueError(f"Invalid win_type {self.win_type}")
        signal = import_optional_dependency(
            "scipy.signal", extra="Scipy is required to generate window weight."
        )
        self._scipy_weight_generator = getattr(signal, self.win_type, None)
        if self._scipy_weight_generator is None:
            raise ValueError(f"Invalid win_type {self.win_type}")

        if isinstance(self.window, BaseIndexer):
            raise NotImplementedError(
                "BaseIndexer subclasses not implemented with win_types."
            )
        if not is_integer(self.window) or self.window < 0:
            raise ValueError("window must be an integer 0 or greater")

        if self.method != "single":
            raise NotImplementedError("'single' is the only supported method type.")
