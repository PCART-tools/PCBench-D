    def _validate_freq(self):
        """
        Validate & return window frequency.
        """
        from pandas.tseries.frequencies import to_offset

        try:
            return to_offset(self.window)
        except (TypeError, ValueError):
            raise ValueError(
                f"passed window {self.window} is not "
                "compatible with a datetimelike "
                "index"
            )
