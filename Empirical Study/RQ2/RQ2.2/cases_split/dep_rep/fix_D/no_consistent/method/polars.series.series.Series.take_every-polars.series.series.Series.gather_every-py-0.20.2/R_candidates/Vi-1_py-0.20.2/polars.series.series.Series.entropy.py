    def entropy(self, base: float = math.e, *, normalize: bool = False) -> float | None:
        """
        Computes the entropy.

        Uses the formula `-sum(pk * log(pk)` where `pk` are discrete probabilities.

        Parameters
        ----------
        base
            Given base, defaults to `e`
        normalize
            Normalize pk if it doesn't sum to 1.

        Examples
        --------
        >>> a = pl.Series([0.99, 0.005, 0.005])
        >>> a.entropy(normalize=True)
        0.06293300616044681
        >>> b = pl.Series([0.65, 0.10, 0.25])
        >>> b.entropy(normalize=True)
        0.8568409950394724

        """
        return (
            self.to_frame()
            .select_seq(F.col(self.name).entropy(base, normalize=normalize))
            .to_series()
            .item()
        )
