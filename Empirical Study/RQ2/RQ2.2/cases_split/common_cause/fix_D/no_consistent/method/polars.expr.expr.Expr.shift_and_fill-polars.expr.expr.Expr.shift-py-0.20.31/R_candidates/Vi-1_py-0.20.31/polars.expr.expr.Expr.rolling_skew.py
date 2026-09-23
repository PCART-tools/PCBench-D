    @unstable()
    def rolling_skew(self, window_size: int, *, bias: bool = True) -> Self:
        """
        Compute a rolling skew.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        The window at a given row includes the row itself and the
        `window_size - 1` elements before it.

        Parameters
        ----------
        window_size
            Integer size of the rolling window.
        bias
            If False, the calculations are corrected for statistical bias.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 4, 2, 9]})
        >>> df.select(pl.col("a").rolling_skew(3))
        shape: (4, 1)
        ┌──────────┐
        │ a        │
        │ ---      │
        │ f64      │
        ╞══════════╡
        │ null     │
        │ null     │
        │ 0.381802 │
        │ 0.47033  │
        └──────────┘

        Note how the values match the following:

        >>> pl.Series([1, 4, 2]).skew(), pl.Series([4, 2, 9]).skew()
        (0.38180177416060584, 0.47033046033698594)
        """
        return self._from_pyexpr(self._pyexpr.rolling_skew(window_size, bias))
