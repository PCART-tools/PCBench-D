    @property
    def cat(self) -> ExprCatNameSpace:
        """
        Create an object namespace of all categorical related methods.

        See the individual method pages for full details

        Examples
        --------
        >>> df = pl.DataFrame({"values": ["a", "b"]}).select(
        ...     pl.col("values").cast(pl.Categorical)
        ... )
        >>> df.select(pl.col("values").cat.set_ordering(ordering="physical"))
        shape: (2, 1)
        ┌────────┐
        │ values │
        │ ---    │
        │ cat    │
        ╞════════╡
        │ a      │
        │ b      │
        └────────┘

        """
        return ExprCatNameSpace(self)
