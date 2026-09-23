    def nan_max(self) -> int | float | date | datetime | timedelta | str:
        """
        Get maximum value, but propagate/poison encountered NaN values.

        This differs from numpy's `nanmax` as numpy defaults to propagating NaN values,
        whereas polars defaults to ignoring them.

        Examples
        --------
        >>> s = pl.Series("a", [1, 3, 4])
        >>> s.nan_max()
        4

        >>> s = pl.Series("a", [1.0, float("nan"), 4.0])
        >>> s.nan_max()
        nan
        """
        return self.to_frame().select_seq(F.col(self.name).nan_max()).item()
