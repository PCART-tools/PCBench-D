    def sem(self, ddof: int = 1, numeric_only: bool = False, *args, **kwargs):
        nv.validate_rolling_func("sem", args, kwargs)
        # Raise here so error message says sem instead of std
        self._validate_numeric_only("sem", numeric_only)
        return self.std(numeric_only=numeric_only, **kwargs) / (
            self.count(numeric_only=numeric_only) - ddof
        ).pow(0.5)
