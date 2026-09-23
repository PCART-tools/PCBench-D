    def validate(self):
        super().validate()

        window = self.window
        if isinstance(window, (list, tuple, np.ndarray)):
            pass
        elif is_integer(window):
            if window <= 0:
                raise ValueError("window must be > 0 ")
            import_optional_dependency(
                "scipy", extra="Scipy is required to generate window weight."
            )
            import scipy.signal as sig

            if not isinstance(self.win_type, str):
                raise ValueError("Invalid win_type {0}".format(self.win_type))
            if getattr(sig, self.win_type, None) is None:
                raise ValueError("Invalid win_type {0}".format(self.win_type))
        else:
            raise ValueError("Invalid window {0}".format(window))
