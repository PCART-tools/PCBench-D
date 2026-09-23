    def pct_change(self, periods=1, fill_method="pad", limit=None, freq=None):
        """Calculate pct_change of each value to previous entry in group"""
        # TODO: Remove this conditional when #23918 is fixed
        if freq:
            return self.apply(
                lambda x: x.pct_change(
                    periods=periods, fill_method=fill_method, limit=limit, freq=freq
                )
            )
        if fill_method is None:  # GH30463
            fill_method = "pad"
            limit = 0
        filled = getattr(self, fill_method)(limit=limit)
        fill_grp = filled.groupby(self.grouper.codes)
        shifted = fill_grp.shift(periods=periods, freq=freq)

        return (filled / shifted) - 1
