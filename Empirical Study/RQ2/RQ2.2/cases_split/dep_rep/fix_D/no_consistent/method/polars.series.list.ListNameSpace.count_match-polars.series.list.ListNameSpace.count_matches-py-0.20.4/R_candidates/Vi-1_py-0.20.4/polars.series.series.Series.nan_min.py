    def nan_min(self) -> int | float | date | datetime | timedelta | str:
        """
        Get minimum value, but propagate/poison encountered NaN values.

        This differs from numpy's `nanmax` as numpy defaults to propagating NaN values,
        whereas polars defaults to ignoring them.

        Examples
        --------
        >>> s = pl.Series("a", [1, 3, 4])
        >>> s.nan_min()
        1

        >>> s = pl.Series("a", [1, float("nan"), 4])
        >>> s.nan_min()
        nan
        """
        return self.to_frame().select_seq(F.col(self.name).nan_min()).item()
