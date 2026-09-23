    def pct_change(self, periods=1, fill_method='pad', limit=None, freq=None):
        """Calculate percent change of each value to previous entry in group"""
        filled = getattr(self, fill_method)(limit=limit)
        shifted = filled.shift(periods=periods, freq=freq)

        return (filled / shifted) - 1
