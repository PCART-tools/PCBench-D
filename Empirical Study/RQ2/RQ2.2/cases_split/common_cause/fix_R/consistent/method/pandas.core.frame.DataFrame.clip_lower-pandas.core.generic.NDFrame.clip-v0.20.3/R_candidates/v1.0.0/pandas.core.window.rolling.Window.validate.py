    def validate(self):
        super().validate()

        window = self.window
        if isinstance(window, BaseIndexer):
            raise NotImplementedError(
                "BaseIndexer subclasses not implemented with win_types."
            )
        elif isinstance(window, (list, tuple, np.ndarray)):
            pass
        elif is_integer(window):
            if window <= 0:
                raise ValueError("window must be > 0 ")
            import_optional_dependency(
                "scipy", extra="Scipy is required to generate window weight."
            )
            import scipy.signal as sig

            if not isinstance(self.win_type, str):
                raise ValueError(f"Invalid win_type {self.win_type}")
            if getattr(sig, self.win_type, None) is None:
                raise ValueError(f"Invalid win_type {self.win_type}")
        else:
            raise ValueError(f"Invalid window {window}")
