    def fillna(self, value, **kwargs):

        # allow filling with integers to be
        # interpreted as nanoseconds
        if is_integer(value):
            # Deprecation GH#24694, GH#19233
            raise TypeError(
                "Passing integers to fillna for timedelta64[ns] dtype is no "
                "longer supported.  To obtain the old behavior, pass "
                "`pd.Timedelta(seconds=n)` instead."
            )
        return super().fillna(value, **kwargs)
