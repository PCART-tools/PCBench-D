    def fillna(self, value, **kwargs):

        # allow filling with integers to be
        # interpreted as nanoseconds
        if is_integer(value):
            # Deprecation GH#24694, GH#19233
            warnings.warn(
                "Passing integers to fillna is deprecated, will "
                "raise a TypeError in a future version.  To retain "
                "the old behavior, pass pd.Timedelta(seconds=n) "
                "instead.",
                FutureWarning,
                stacklevel=6,
            )
            value = Timedelta(value, unit="s")
        return super().fillna(value, **kwargs)
