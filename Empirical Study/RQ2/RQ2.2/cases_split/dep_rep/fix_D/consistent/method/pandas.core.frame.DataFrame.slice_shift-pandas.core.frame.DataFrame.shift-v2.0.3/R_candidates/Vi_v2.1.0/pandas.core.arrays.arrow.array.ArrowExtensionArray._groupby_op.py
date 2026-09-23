    def _groupby_op(
        self,
        *,
        how: str,
        has_dropped_na: bool,
        min_count: int,
        ngroups: int,
        ids: npt.NDArray[np.intp],
        **kwargs,
    ):
        if isinstance(self.dtype, StringDtype):
            return super()._groupby_op(
                how=how,
                has_dropped_na=has_dropped_na,
                min_count=min_count,
                ngroups=ngroups,
                ids=ids,
                **kwargs,
            )

        masked = self._to_masked()

        result = masked._groupby_op(
            how=how,
            has_dropped_na=has_dropped_na,
            min_count=min_count,
            ngroups=ngroups,
            ids=ids,
            **kwargs,
        )
        if isinstance(result, np.ndarray):
            return result
        return type(self)._from_sequence(result, copy=False)
