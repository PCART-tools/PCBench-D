    @final
    def _python_apply_general(
        self,
        f: Callable,
        data: DataFrame | Series,
        not_indexed_same: bool | None = None,
    ) -> DataFrame | Series:
        """
        Apply function f in python space

        Parameters
        ----------
        f : callable
            Function to apply
        data : Series or DataFrame
            Data to apply f to
        not_indexed_same: bool, optional
            When specified, overrides the value of not_indexed_same. Apply behaves
            differently when the result index is equal to the input index, but
            this can be coincidental leading to value-dependent behavior.

        Returns
        -------
        Series or DataFrame
            data after applying f
        """
        values, mutated = self.grouper.apply(f, data, self.axis)

        if not_indexed_same is None:
            not_indexed_same = mutated or self.mutated

        return self._wrap_applied_output(
            data, values, not_indexed_same=not_indexed_same
        )
