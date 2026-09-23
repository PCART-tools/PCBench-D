    def mode(self, dropna: bool = True) -> Categorical:
        """
        Returns the mode(s) of the Categorical.

        Always returns `Categorical` even if only one value.

        Parameters
        ----------
        dropna : bool, default True
            Don't consider counts of NaN/NaT.

        Returns
        -------
        modes : `Categorical` (sorted)
        """
        warn(
            "Categorical.mode is deprecated and will be removed in a future version. "
            "Use Series.mode instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self._mode(dropna=dropna)
